import React from 'react';

const Filter = ({ onFilterChange }) => {
  return (
    <div className="filter">
      <label>
        Category:
        <input type="text" onChange={(e) => onFilterChange('category', e.target.value)} />
      </label>
      <label>
        Company:
        <input type="text" onChange={(e) => onFilterChange('company', e.target.value)} />
      </label>
      <label>
        Price Range:
        <input type="text" onChange={(e) => onFilterChange('price', e.target.value)} />
      </label>
      <label>
        Rating:
        <input type="text" onChange={(e) => onFilterChange('rating', e.target.value)} />
      </label>
      <label>
        Availability:
        <select onChange={(e) => onFilterChange('availability', e.target.value)}>
          <option value="">All</option>
          <option value="true">In Stock</option>
          <option value="false">Out of Stock</option>
        </select>
      </label>
    </div>
  );
};

export default Filter;
