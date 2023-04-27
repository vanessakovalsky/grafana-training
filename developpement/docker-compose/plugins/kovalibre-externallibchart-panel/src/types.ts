type SeriesSize = 'sm' | 'md' | 'lg';

export interface SimpleOptions {
  text: string;
  showSeriesCount: boolean;
  seriesCountSize: SeriesSize;
}

export class VictoryData {
  constructor(
    public x: number, 
    public y: number,
  ) {
  }
}
