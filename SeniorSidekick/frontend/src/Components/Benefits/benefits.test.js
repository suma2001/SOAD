import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { queryByTestId, render } from '@testing-library/react';
import Benefits from './benefits';

test('renders successfully', () => {
  render(<Benefits />);
});

test('renders the first benefit content correctly', () => {
    const root = document.createElement("div");
    ReactDOM.render(<Benefits />, root);
    expect(queryByTestId(root, 'goal')).toHaveTextContent("Goal");
    expect(queryByTestId(root, 'goal_text')).toHaveTextContent("Connect elderly with young adults. Should add some more content in this part");
})

test('renders the second benefit content correctly', () => {
    const root = document.createElement("div");
    ReactDOM.render(<Benefits />, root);
    expect(queryByTestId(root, 'interactive')).toHaveTextContent("Interactive");
    expect(queryByTestId(root, 'interactive_text')).toHaveTextContent("User-friendly UI to make it accessible and easy for the seniors to interact with the website");
})

test('renders the third benefit content correctly', () => {
    const root = document.createElement("div");
    ReactDOM.render(<Benefits />, root);
    expect(queryByTestId(root, 'connectivity')).toHaveTextContent("Connectivity");
    expect(queryByTestId(root, 'connectivity_text')).toHaveTextContent("Help foster the connectivity and sharing of meaningful experiences");
})


test('renders the solution content correctly', () => {
    const root = document.createElement("div");
    ReactDOM.render(<Benefits />, root);
    expect(queryByTestId(root, 'solution')).toHaveTextContent("SOLUTION");
    expect(queryByTestId(root, 'potential')).toHaveTextContent("Unlock the Potential");
    expect(queryByTestId(root, 'solution_text')).toHaveTextContent("A website that connects seniors with young volunteers to help them with their daily tasks, activities and also have a buddy to talk to when they want company");
})