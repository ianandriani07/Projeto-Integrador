import "./styles/Header.scss";
import React from 'react';

interface headerProp {
    title?: string,
    logout: boolean
}

export const Header: React.FC<headerProp> = ({ title, logout = false }) => {
    return (
        <header>
            <button className="no-style logout-button">
                {logout ? <><span>&#10005;</span>Logout</> : <>Return</>}
            </button>
            <div className="align-in-row-left">
                <img className="logo" src="/static/icons/backbone.svg" />
                {title != undefined ? <h1 className="title">{title}</h1> : ""}
            </div>
        </header>
    )
}