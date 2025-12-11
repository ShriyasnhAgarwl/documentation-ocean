Functionality Flow  - >
Frontend:
- Max size: 800 KB per image
- Tries WebP first, falls back to JPEG
- Progressively reduces quality (85% → 70% → 50% → 20%) until size met
- Shows warning if image exceeds target

Backend:
- Server-side re-compression with Sharp (image processing)
- Metadata Stripping - Remove EXIF/GPS data
- Enforces 800 KB limit
- Tries quality levels: 85, 75, 65, 55, 45, 35, 25, 20
- Rejects images that can't meet size requirement
