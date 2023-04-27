import { PanelPlugin, FieldColorModeId } from '@grafana/data';
import { SimpleOptions } from './types';
import { DemoTimeSeriePanel } from './components/DemoTimeSeriePanel';

export const plugin = new PanelPlugin<SimpleOptions>(DemoTimeSeriePanel)
.useFieldConfig({
  standardOptions: {
    color: {
      defaultValue: {
        mode: FieldColorModeId.ContinuousGrYlRd,
      },
    },
  },
  useCustomConfig: (builder) => {
    builder
      
  },
})
.setPanelOptions((builder) => {
  return builder
    
});
