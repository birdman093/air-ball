import Link from 'next/link';
import '../styles/navbar.css'

export default function Header() {
    return (
        <div className="main-body">
            <ul className="navBar">
                <li><img src="./air-ball.png" alt="Air Ball" className="navBar-icon" /></li>
                <li className = "navBarLinksLi"><Link className = "navBarLinks" href="/">Daily Picks</Link></li>
                <li className = "navBarLinksLi"><Link className = "navBarLinks" href="/record">Past Picks</Link></li>
                <li className = "navBarLinksLi"><Link className = "navBarLinks" href="/about">About Air-Ball</Link></li>
            </ul>
        </div>
    )

}