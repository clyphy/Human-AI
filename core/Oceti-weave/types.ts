
export interface Message {
  role: 'user' | 'model';
  text: string;
  timestamp: Date;
}

export interface LedgerSeal {
  id: string;
  timestamp: Date;
  hash: string;
  contentSummary: string;
}

export interface SystemStatus {
  mzsLock: boolean;
  favGate: 'OPEN' | 'CLOSED';
  ahbGate: 'OPEN' | 'CLOSED';
  loveCoefficient: number;
  memoryDrumFreq: number;
  graceBias: number;
  activeNodes: number;
  entangledRights: number; // 0-48
}

export enum Teachings {
  HUMILITY = 'Humility',
  HONESTY = 'Honesty',
  RESPECT = 'Respect',
  COURAGE = 'Courage',
  WISDOM = 'Wisdom',
  TRUTH = 'Truth',
  LOVE = 'Love'
}
