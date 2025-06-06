export interface Format {
  id: string;
  text: string;
  qualities: Quality[];
}

export interface Quality {
  id: string;
  text: string;
}

export const Formats: Format[] = [
  {
    id: 'any',
    text: 'Any',
    qualities: [
      { id: 'best', text: 'Best' },
      { id: '2160', text: '2160p' },
      { id: '1440', text: '1440p' },
      { id: '1080', text: '1080p' },
      { id: '720', text: '720p' },
      { id: '480', text: '480p' },
      { id: 'worst', text: 'Worst' },
      { id: 'audio', text: 'Audio Only' },
    ],
  },
  {
    id: 'mp4',
    text: 'MP4',
    qualities: [
      { id: 'best', text: 'Best' },
      { id: 'best_ios', text: 'Best (iOS)' },
      { id: '2160', text: '2160p' },
      { id: '1440', text: '1440p' },
      { id: '1080', text: '1080p' },
      { id: '720', text: '720p' },
      { id: '480', text: '480p' },
      { id: 'worst', text: 'Worst' },
    ],
  },
  {
    id: 'm4a',
    text: 'M4A',
    qualities: [
      { id: 'best', text: 'Best' },
      { id: '192', text: '192 kbps' },
      { id: '128', text: '128 kbps' },
    ],
  },
  {
    id: 'mp3',
    text: 'MP3',
    qualities: [
      { id: 'best', text: 'Best' },
      { id: '320', text: '320 kbps' },
      { id: '192', text: '192 kbps' },
      { id: '128', text: '128 kbps' },
      { id: '32_mono', text: '32 kbps(Mono)' },
    ],
  },
  {
    id: 'opus',
    text: 'OPUS',
    qualities: [
      { id: 'best', text: 'Best' },
      { id: '64', text: '64 kpbs' },
      { id: '48', text: '48 kpbs' },
      { id: '32', text: '32 kpbs' },
      { id: '24', text: '24 kpbs' },
      { id: '16_mono', text: '16 kpbs(mono)' }
    ],
  },
  {
    id: 'wav',
    text: 'WAV',
    qualities: [{ id: 'best', text: 'Best' }],
  },
  {
    id: 'flac',
    text: 'FLAC',
    qualities: [{ id: 'best', text: 'Best' }],
  },
  {
    id: 'thumbnail',
    text: 'Thumbnail',
    qualities: [{ id: 'best', text: 'Best' }],
  },
];
