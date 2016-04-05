'use strict';
var React = require('react');
var cloneWithProps = require('react/lib/cloneWithProps');
var {DropdownMenu} = require('./dropdown-menu');

var Navbar = module.exports.Navbar = React.createClass({
    propTypes: {
        brand: React.PropTypes.oneOfType([ // String or component to display for the brand with class `navbar-brand`
            React.PropTypes.string,
            React.PropTypes.object
        ]),
        brandlink: React.PropTypes.string, // href for clicking brand
        label: React.PropTypes.string.isRequired, // id for nav; unique on page
        navClasses: React.PropTypes.string // CSS classes for <nav> in addition to "navbar"; default to "navbar-default"
    },
    
    getInitialState: function() {
        return {
            expanded: false, // True if mobile version of menu is expanded
            openDropdown: '' // String identifier of currently opened DropdownMenu
        };  
    },
    
    componentDidMount: function() {
        // Add a click handler to the DOM document -- the entire page
        document.addEventListener('click', this.documentClickHandler);
    },

    componentWillUnmount: function() {
        // Remove the DOM document click handler now that the DropdownButton is going away.
        document.removeEventListener('click', this.documentClickHandler);
    },

    documentClickHandler: function() {
        // A click outside the DropdownButton closes the dropdown
        this.setState({openDropdown: ''});
    },

    collapseClick: function(e) {
        // Click on the Navbar mobile "collapse" button
        this.setState({expanded: !this.state.expanded});
    },

    dropdownClick: function(dropdownId, e) {
        // After clicking the dropdown trigger button, don't allow the event to bubble to the rest of the DOM.
        e.nativeEvent.stopImmediatePropagation();
        this.setState({openDropdown: dropdownId === this.state.dropdownId ? '' : dropdownId});
    },

    render: function() {
        var {brand, brandlink, label, navClasses} = this.props;

        // Add the `openDropdown` property to any <DropdownMenu> child components
        var children = React.Children.map(this.props.children, child => {
            if (child.type === NavItem.type) {
                return cloneWithProps(child, {
                    openDropdown: this.state.openDropdown,
                    dropdownClick: this.dropdownClick
                });
            }
            return child;
        });

        return (
            <nav className={'navbar ' + (navClasses ? navClasses : 'navbar-default')}>
                <div className="navbar-header">
                    <button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target={label} aria-expanded={this.state.expanded} onClick={this.collapseClick}>
                        <span className="sr-only">Toggle navigation</span>
                        <span className="icon-bar"></span>
                        <span className="icon-bar"></span>
                        <span className="icon-bar"></span>
                    </button>
                    {brand ?
                        <a className="navbar-brand" href={brandlink}>{brand}</a>
                    : null}
                </div>
                
                <div className="collapse navbar-collapse" id={label}>
                    <ul className="nav navbar-nav">
                        {children}
                    </ul>
                </div>
            </nav>
        );
    }
});


var NavItem = module.exports.NavItem = React.createClass({
    propTypes: {
        dropdownId: React.PropTypes.string, // If this item has a dropdown, this ID helps manage it; must be unique
        dropdownTitle: React.PropTypes.string, // If this item has a dropdown, this is the title
        openDropdown: React.PropTypes.string, // dropdownId of currently open dropdown; '' if all closed. Passed by parent Navbar
        dropdownClick: React.PropTypes.func // Function to call when dropdown title clicked. Passed by parent Navbar
    },

    render: function() {
        var {dropdownId, dropdownTitle, openDropdown, dropdownClick} = this.props;
        var dropdownOpen = dropdownId && (openDropdown === dropdownId);

        return (
            <li className={dropdownId ? ('dropdown' + (dropdownOpen ? ' open' : '')) : ''}>
                {dropdownTitle ?
                    <a href="#" className="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded={dropdownOpen} onClick={dropdownClick.bind(null, dropdownId)}>
                        {dropdownTitle}
                    </a>
                : null}
                {this.props.children}
            </li>
        );
    }
});
