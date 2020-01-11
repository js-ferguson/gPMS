const categorySelect = () => {
    const select = document.getElementById("selector");
    const value = document.getElementById("category-dropdown").value;
    if (value == "spell") {
        url = 'http://www.dnd5eapi.co/api/spells';
        searchType = 'spells';
    } else {
        url = 'http://www.dnd5eapi.co/api/monsters';
        searchType = 'monsters';
    }
    removeOptions(select);
};
