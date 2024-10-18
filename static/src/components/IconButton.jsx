import "./styles/IconButtonStyle.scss";
import React, { useState, useEffect } from 'react';

export function IconButton({ iconPath, children, className, noDefaults = false }) {
    return (
        <>
            <button className={(!noDefaults ? "icon-button-align-icon " + className : className)}>
                <img src={iconPath} />
                {children}
            </button>
        </>
    )
}