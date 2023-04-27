import { screen } from '@testing-library/react'
import SimplePanel from './SimplePanel';
import { render } from "react-dom";

test('Mon super test', async() => {
    render(SimplePanel);
    expect(screen.getByText('/Bienvenue/')).toBeInDocument();
});
