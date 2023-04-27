type SeriesSize = 'sm' | 'md' | 'lg';

export interface SimpleOptions {
  text: string;
  showSeriesCount: boolean;
  seriesCountSize: SeriesSize;
  demoNumber: number;
}


export class ColData {
  constructor(
    public name: string,
    public displayName: string,
    public type: string,
    public values: (number | string | null)[],
  ) {
  }
}