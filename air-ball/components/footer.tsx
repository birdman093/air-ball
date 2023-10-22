import React, {useState} from 'react';
import '../styles/footer.css';

function Footer() {
    const [isOn, setIsOn] = useState(false);

    const handleClick = () => {
        const querySelect = document.querySelector(':root');
        let cs;
        if (querySelect) {
            cs = getComputedStyle(querySelect);
        } else {
            return;
        }
        
        let bg_color; let text_color; let header_color; let github_icon;
        let bg_border_color;
        if (isOn){
            bg_color = cs.getPropertyValue('--dark-mode-bg');
            bg_border_color = cs.getPropertyValue('--dark-mode-header-border');
            text_color = cs.getPropertyValue('--dark-mode-text');
            header_color = cs.getPropertyValue('--dark-mode-header');
            github_icon = cs.getPropertyValue('--dark-mode-gh-icon');
        } 
        else 
        {
            bg_color = cs.getPropertyValue('--light-mode-bg');
            bg_border_color = cs.getPropertyValue('--light-mode-header-border');
            text_color = cs.getPropertyValue('--light-mode-text');
            header_color = cs.getPropertyValue('--light-mode-header');
            github_icon = cs.getPropertyValue('--light-mode-gh-icon');
        }
        document.documentElement.style.setProperty('--bg-color', bg_color);
        document.documentElement.style.setProperty('--header-border-color', bg_border_color);
        document.documentElement.style.setProperty('--text-color', text_color);
        document.documentElement.style.setProperty('--header-bg-color', header_color);
        document.documentElement.style.setProperty('--github-icon', github_icon);
        
        setIsOn(!isOn);
    }

    return (
        <footer className="footer">
            <p className="rights">© 2023 Feathers Codes. All Rights Reserved.</p>
            <div className="switch-container">
                <label className="switch-label">Light Mode</label>
                <label className="switch">
                    <input type="checkbox"  onClick={handleClick}></input>
                    <span className="slider round"></span>
                </label>
            </div>
        </footer>
    );
}

export default Footer;
