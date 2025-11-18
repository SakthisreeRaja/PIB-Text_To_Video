import { useState } from "react";
import './Searchbar.css';
import { FaSearch } from "react-icons/fa";
import { useTranslation } from 'react-i18next';

function SearchBar({ setSearchTerm }) {

    const { t } = useTranslation();
    const [query, setQuery] = useState('');

    return (
        <div className="search-bar">
            <FaSearch className="search-icon" />
            <input
                type="text"
                placeholder={t('search_placeholder')}
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