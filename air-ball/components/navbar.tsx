import Link from 'next/link';
import '../styles/navbar.css'

export default function Header() {
    return (
        <div className="main-body">
            <ul className="navBar">
                <li><img src="./air-ball.png" alt="Air Ball" className="navBar-icon" /></li>
                <li className = "navBarLinksLi"><Link className = "navBarLinks" href="/today">Today's Games</Link></li>
                <li className = "navBarLinksLi"><Link className = "navBarLinks" href="/past">Past Games</Link></li>
                <li className = "navBarLinksLi"><Link className = "navBarLinks" href="/record">Air-Ball Record</Link></li>
            </ul>
        </div>
    )

}