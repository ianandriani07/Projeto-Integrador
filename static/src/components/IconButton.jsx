require("./styles/IconButtonStyle.scss");
const React = require('react');
const { useState, useEffect } = React;

function IconButton({ iconPath, children, className, noDefaults = false }) {
    return (
        <>
            <button className={(!noDefaults ? "icon-button-align-icon " + className : className)}>
                <img src={iconPath} />
                {children}
            </button>
        </>
    )
}