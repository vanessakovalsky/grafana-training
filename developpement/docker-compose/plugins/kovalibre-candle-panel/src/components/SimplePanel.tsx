import React from 'react';
import { PanelProps } from '@grafana/data';
import { SimpleOptions } from 'types';
import { VictoryCandlestick } from 'victory-candlestick';
import { VictoryChart, VictoryAxis, VictoryTheme } from 'victory';

interface Props extends PanelProps<SimpleOptions> {}

export const SimplePanel: React.FC<Props> = ({ options, data, width, height }) => {

  return (
      <VictoryChart
          theme={VictoryTheme.material}
          domainPadding={{ x: 25 }}
          scale={{ x: "time" }}
          width={width}
          height={height}
        >
        <VictoryAxis tickFormat={(t) => `${t.getDate()}/${t.getMonth()}`}/>
        <VictoryAxis dependentAxis/>
        <VictoryCandlestick
          candleColors={{ positive: "#5f5c5b", negative: "#c43a31" }}
          data={[
            {x: new Date(2023, 6, 1), open: 5, close: 10, high: 15, low: 0},
            {x: new Date(2023, 6, 2), open: 10, close: 15, high: 20, low: 5},
            {x: new Date(2023, 6, 3), open: 15, close: 20, high: 22, low: 10},
            {x: new Date(2023, 6, 4), open: 20, close: 10, high: 25, low: 7},
            {x: new Date(2023, 6, 5), open: 10, close: 8, high: 15, low: 5}
          ]}
        />
      </VictoryChart>
  );
};
