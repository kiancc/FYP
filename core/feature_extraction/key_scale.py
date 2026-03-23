import essentia
import essentia.streaming as es

# note we dont use sr at all, its just so the method signature matches for the librosa method calls in pipeline.py.
# not that elegant but will fix later, it works for now.

def extract_essentia_key_scale(audio, file_id):
    key, scale, strength = essentia_detect_key(audio)
    
    return {
        'file_id': file_id,
        'key': key,
        'scale': scale,
        'strength': strength
    }
    
# Taken from https://essentia.upf.edu/tutorial_tonal_hpcpkeyscale.html
def essentia_detect_key(audio):

    # Initialize algorithms we will use.
    loader = es.VectorInput(audio)
    framecutter = es.FrameCutter(frameSize=4096, hopSize=2048, silentFrames='noise')
    windowing = es.Windowing(type='blackmanharris62')
    spectrum = es.Spectrum()
    spectralpeaks = es.SpectralPeaks(orderBy='magnitude',
                                      magnitudeThreshold=0.00001,
                                      minFrequency=20,
                                      maxFrequency=3500,
                                      maxPeaks=60)

    # Use default HPCP parameters for plots.
    # However we will need higher resolution and custom parameters for better Key estimation.

    hpcp = es.HPCP()
    hpcp_key = es.HPCP(size=36, # We will need higher resolution for Key estimation.
                        referenceFrequency=440, # Assume tuning frequency is 44100.
                        bandPreset=False,
                        minFrequency=20,
                        maxFrequency=3500,
                        weightType='cosine',
                        nonLinear=False,
                        windowSize=1.)

    key = es.Key(profileType='edma', # Use profile for electronic music.
                  numHarmonics=4,
                  pcpSize=36,
                  slope=0.6,
                  usePolyphony=True,
                  useThreeChords=True)

    # Use pool to store data.
    pool = essentia.Pool()

    # Connect streaming algorithms.
    loader.data >> framecutter.signal
    framecutter.frame >> windowing.frame >> spectrum.frame
    spectrum.spectrum >> spectralpeaks.spectrum
    spectralpeaks.magnitudes >> hpcp.magnitudes
    spectralpeaks.frequencies >> hpcp.frequencies
    spectralpeaks.magnitudes >> hpcp_key.magnitudes
    spectralpeaks.frequencies >> hpcp_key.frequencies
    hpcp_key.hpcp >> key.pcp
    hpcp.hpcp >> (pool, 'tonal.hpcp')
    key.key >> (pool, 'tonal.key_key')
    key.scale >> (pool, 'tonal.key_scale')
    key.strength >> (pool, 'tonal.key_strength')

    # Run streaming network.
    essentia.run(loader)

    # print("Estimated key and scale:", pool['tonal.key_key'] + " " + pool['tonal.key_scale'])

    return (pool['tonal.key_key'], pool['tonal.key_scale'], pool['tonal.key_strength'])