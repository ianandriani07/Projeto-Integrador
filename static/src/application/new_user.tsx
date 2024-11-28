import "../styles/new_user.scss";
const React = require('react');
const { createRoot } = require('react-dom/client');
import { Header } from "../components/Header.tsx";

function NewUser() {
    return (
        <>
            <Header title='Criar Usuario”' />
        </>
    )
};

const root = document.getElementById('base-new-user');
const rootElement = createRoot(root);
rootElement.render(<NewUser />);