import React, { useState } from 'react';
import { PanelProps } from '@grafana/data';
import { SimpleOptions, ColData } from 'types';
import { Button, Input } from '@grafana/ui';

interface Props extends PanelProps<SimpleOptions> {}

export const SimplePanel: React.FC<Props> = ({ options, data, width, height }) => {
  const frame = data.series[0];

  const colData = new Array(0);

  frame.fields.forEach((field) => {
    colData.push(new ColData(
      field.name,
      field.config?.displayName || field.name,
      field.type,
      field.values.toArray().map((v) => v as number),
    ));
  });

  console.log(colData);


  const [compteur, setCompteur] = useState(0);
  
  const [ user, setUser] = useState({
    nom: 'toto',
    age: 42,
  });

  const handleClick = ((e: React.MouseEvent<HTMLOrSVGElement>) =>{
    console.log('passe dans le handleclick')
    setCompteur(compteur +1);
    console.log(compteur);
  } );



  const handleInput = ((e: React.ChangeEvent<HTMLInputElement>) => {
    console.log(e);
    setUser({
      ...user,
      nom: e.target.value
    }
    )
  });


  return (
    <div>
    <h1>Bienvenue</h1>
    <div>{ options.text }</div>
    <div>{ options.demoNumber }</div>
    <Button size='lg' onClick={handleClick}>Enregistrer</Button>
    <div>{compteur}</div>
    <Input onChange={handleInput}
    />
    <div>{user.nom}</div>

    <table>
      <thead>
        <tr>
        { colData.map((field) => (
              <th key={field}>{field.displayName}</th>
          ))}
        </tr>
          
      </thead>
      <tbody>
        { colData.map((field) => (
            field.values.map((value: number, index: number) => 
            <tr key={index}>
              <td key={index}>{value}</td>
            </tr>

            )
          ))}
      </tbody>
    </table>
    </div>
  );
  };
