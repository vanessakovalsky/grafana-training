import React from 'react';
import { PanelProps } from '@grafana/data';
import { SimpleOptions, VictoryData } from 'types';
import { css, cx } from '@emotion/css';
import { useStyles2 } from '@grafana/ui';
import { VictoryChart, VictoryLine, VictoryTheme } from 'victory';


interface Props extends PanelProps<SimpleOptions> {}

const getStyles = () => {
  return {
    wrapper: css`
      font-family: Open Sans;
      position: relative;
    `,
    svg: css`
      position: absolute;
      top: 0;
      left: 0;
    `,
    textBox: css`
      position: absolute;
      bottom: 0;
      left: 0;
      padding: 10px;
    `,
  };
};

export const SimplePanel: React.FC<Props> = ({ options, data, width, height }) => {
  const styles = useStyles2(getStyles);

  const length_data = data.series[0].length

  const field_x = data.series[0].fields.find((field) => field.name === 'ID')
  const values_x = field_x?.values.toArray() || [42,45,87,88];

  const field_y = data.series[0].fields.find((field) => field.name === 'comment_count')
  const values_y = field_y?.values.toArray() || [42,45,87,88];

  const victory_data = new Array(0);

  let i = 0
  while (i < length_data) {
    victory_data.push(
      new VictoryData(
        values_x[i],
        values_y[i],
      ));
    i = i+1;
  };

  return (
    <div
      className={cx(
        styles.wrapper,
        css`
          width: ${width}px;
          height: ${height}px;
        `
      )}
    >
     <VictoryChart
        theme={VictoryTheme.material}
      >
        <VictoryLine
          style={{
            data: { stroke: "#c43a31" },
            parent: { border: "1px solid #ccc"}
          }}
          data={ victory_data }
          scale={{x: 'log', y: 'linear'}}
        />
        <VictoryLine
          style={{
            data: { stroke: "#c43a31" },
            parent: { border: "1px solid #ccc"}
          }}
          data={[
            { x: 1, y: 2 },
            { x: 2, y: 3 },
            { x: 3, y: 5 },
            { x: 4, y: 4 },
            { x: 5, y: 7 }
          ]}
          scale={{x: 'log', y: 'linear'}}
        />
        <VictoryLine
          style={{
            data: { stroke: options.text },
            parent: { border: "1px solid #ccc"}
          }}
          data={ victory_data }
          scale={{x: 'log', y: 'linear'}}
        />
      </VictoryChart>

      <div className={styles.textBox}>
        {options.showSeriesCount && <div>Number of series: {data.series.length}</div>}
        <div>Text option value: {options.text}</div>
      </div>
    </div>
  );
};
