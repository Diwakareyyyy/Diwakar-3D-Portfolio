# Check if WebM has AlphaMode in Video element (0x53C0 in Matroska/WebM)
with open('1000306733-Picsart-BackgroundRemover.webm', 'rb') as f:
    data = f.read(100000) # Read first 100KB header

print('VP8/VP9/AV1 codec search:')
if b'V_VP8' in data:
    print('Codec: VP8')
elif b'V_VP9' in data:
    print('Codec: VP9')
elif b'V_AV1' in data:
    print('Codec: AV1')
else:
    print('Codec not immediately found in first 100KB')

# Search for AlphaMode tag: 0x53, 0xC0
idx = data.find(b'\x53\xc0')
print('AlphaMode (0x53C0) found at offset:', idx)
if idx != -1:
    val = data[idx:idx+4]
    print('AlphaMode byte sequence:', [hex(b) for b in val])
