import "../styles/hub.scss";
import React from 'react';
import { createRoot } from 'react-dom';

function Hub() {
    return (
        <h1>Hello, World!</h1>
    )
};

const root = document.getElementById('base-hub');
const rootElement = createRoot(root);
rootElement.render(<Hub />);