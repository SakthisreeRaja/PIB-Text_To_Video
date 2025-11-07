import { useState } from "react";
import './Searchbar.css';

function SearchBar({ setSearchTerm }) {

    const [query, setQuery] = useState('');

    return (
        <div className="search-bar">
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