import "./styles/Header.scss";
const React = require('react');

interface headerProp {
    title?: string
}

export const Header: React.FC<headerProp> = ({ title }) => {
    return (
        <header>
            <button className="no-style logout-button">
                <span>&#10005;</span>Logout
            </button>
            <div className="align-in-row-left">
                <img className="logo" src="/static/icons/backbone.svg" />
                {title != undefined ? <h1 className="title">{title}</h1> : ""}
            </div>
        </header>
    )
}