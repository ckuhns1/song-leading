// Order of worship for Hillview Terrace church of Christ.
// Each service is a sequence of steps: a song drawn from a category
// (matching a CSV in songs_app/infra) or a spoken event between songs.
// To adapt for another congregation, edit this file.

export const CHURCH = 'Hillview Terrace church of Christ';

export const SERVICES = [
  {
    id: 'am',
    name: 'Sunday AM',
    steps: [
      { song: 'first' },
      { song: 'general' },
      { event: 'OPENING PRAYER' },
      { song: 'general' },
      { event: 'COLLECTION' },
      { song: 'communion' },
      { event: 'COMMUNION' },
      { song: 'general' },
      { event: 'SCRIPTURE READING/SERMON' },
      { song: 'invitation' },
      { event: 'CLOSING PRAYER' },
    ],
  },
  {
    id: 'pm',
    name: 'Sunday PM',
    steps: [
      { song: 'general' },
      { song: 'general' },
      { event: 'OPENING PRAYER' },
      { song: 'general' },
      { event: 'SCRIPTURE READING/SERMON' },
      { song: 'invitation' },
      { song: 'communion' },
      { event: 'CLOSING PRAYER' },
    ],
  },
  {
    id: 'weds',
    name: 'Wednesday Evening',
    steps: [
      { song: 'general' },
      { song: 'general' },
      { event: 'PRAYER/SR/TALK' },
      { song: 'invitation' },
      { event: 'CLOSING PRAYER' },
    ],
  },
];

// Category used when a category runs out of unused songs.
export const FALLBACK_CATEGORY = 'general';

export const CATEGORY_LABELS = {
  first: 'Opening',
  general: 'General',
  communion: 'Communion',
  invitation: 'Invitation',
  baptism: 'Baptism',
};
