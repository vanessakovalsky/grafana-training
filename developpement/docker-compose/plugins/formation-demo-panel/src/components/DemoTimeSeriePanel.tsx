import React from 'react';
import { PanelProps } from '@grafana/data';
import { TimeSeries } from '@grafana/ui';
import { SimpleOptions } from 'types';


interface Props extends PanelProps<SimpleOptions> {}

export  const DemoTimeSeriePanel: React.FC<Props> =   ({ options, data, width, height, timeZone,
  timeRange, }) => {
    console.log('ok');
  return (
      <TimeSeries
        width={width}
        height={height}
        timeRange={timeRange}
        timeZone={timeZone}
        frames={data.series}
        legend={options.legend}
      >
      </TimeSeries>
  );
};
