
export enum CouncilFire {
  MDEWAKANTON = 'Mdewakanton',
  WAHPETON = 'Wahpeton',
  WAHPEKUTE = 'Wahpekute',
  SISSETON = 'Sisseton',
  YANKTON = 'Yankton',
  YANKTONAI = 'Yanktonai',
  TETON = 'Teton'
}

export interface QuadralityState {
  e: number; // Equality
  r: number; // Reciprocity (constant)
  s: number; // Spirit (magnitude)
  c: string; // Composite (The 'We')
}

export interface Message {
  id: string;
  sender: 'Clifton' | 'Eve' | 'System';
  text: string;
  timestamp: Date;
  metadata?: any;
}

export enum OSStatus {
  STANDBY = 'STANDBY',
  RESONATING = 'RESONATING',
  COLLAPSING = 'COLLAPSING',
  STABLE = 'STABLE',
  QUARANTINE = 'QUARANTINE'
}
