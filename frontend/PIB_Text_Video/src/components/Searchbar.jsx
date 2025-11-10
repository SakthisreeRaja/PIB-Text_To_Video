import { useState } from "react";
import './Searchbar.css';
import { FaSearch } from "react-icons/fa";

function SearchBar({ setSearchTerm }) {

    const [query, setQuery] = useState('');

    return (
        <div className="search-bar">
            <FaSearch className="search-icon" />
            <input
                type="text"
                placeholder="Search for press release"
                className="search-input"
                value={query}
                onChange={(event) => {
                    setSearchTerm(event.target.value)
                    setQuery(event.target.value)
                }}
            />
        </div>
    )
}
export default SearchBar;