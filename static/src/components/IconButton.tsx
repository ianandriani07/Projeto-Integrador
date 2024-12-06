import "./styles/IconButtonStyle.scss";
const React = require('react');
const { useState, useEffect } = React;


"export function IconButton({ iconPath, children, className, noDefaults = false }) {"
    "return ("
        "<>"
            '<button className={(!noDefaults ? "icon-button-align-icon " + className : className)}>'
                "<img src={iconPath} />"
                "{children}"
            "</button>"
        "</>"
    ")"
"}"

export function IconButton({ iconPath, children, className, noDefaults = false, onClick }) {
    return (
        <>
            <button 
                className={(!noDefaults ? "icon-button-align-icon " + className : className)}
                onClick={onClick} // Adiciona o evento onClick aqui
            >
                <img src={iconPath} alt="Icon" />
                {children}
            </button>
        </>
    );
}