import React from 'react';
import { PanelProps } from '@grafana/data';
import { SimpleOptions } from 'types';

interface Props extends PanelProps<SimpleOptions> {}

export const SimplePanel: React.FC<Props> = ({ options, data, width, height }) => {
  const valueField = data.series[0].fields.find((field) => field.type === 'number');
  return(
    <div style={{ overflow: 'auto', width, height}}>
        <h1>Bienvenue dans mon panel</h1>
        <div>Text option value: {options.text}</div>
        <div>My number value {options.myNumber}</div>
        <div>
          {valueField.values}
        </div>
    </div>
  )

};
