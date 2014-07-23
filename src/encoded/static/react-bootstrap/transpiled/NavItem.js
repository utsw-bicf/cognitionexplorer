"use strict";
/** @jsx React.DOM */

var React = require("react");
var classSet = require("react/lib/cx");
var BootstrapMixin = require("./BootstrapMixin")["default"];
var DropdownStateMixin = require("./DropdownStateMixin")["default"];

var NavItem = React.createClass({displayName: 'NavItem',
  mixins: [BootstrapMixin, DropdownStateMixin],

  propTypes: {
    onSelect: React.PropTypes.func,
    active: React.PropTypes.bool,
    disabled: React.PropTypes.bool,
    href: React.PropTypes.string,
    title: React.PropTypes.string,
    trigger: React.PropTypes.string,
    dropdown: React.PropTypes.bool
  },

  getDefaultProps: function () {
    return {
      href: '#'
    };
  },

  getInitialState: function() {
    return {
      focused: false
    };
  },

  render: function () {
    var classes = {
      'active': this.props.active,
      'disabled': this.props.disabled,
      'dropdown': this.props.dropdown,
      'open': this.state.open
    };

    var anchorClass = this.props.dropdown ? 'dropdown-toggle' : '';

    return (
      React.DOM.li( {className:classSet(classes)}, 
        this.transferPropsTo(
        React.DOM.a(
          {className:anchorClass,
          onClick:this.handleClick,
          onFocus:this.handleFocus,
          onBlur:this.handleBlur,
          onKeyDown:this.handleKeyDown,
          ref:"anchor"}, 
          this.props.dropdown ? React.DOM.span(null, this.props.children[0],React.DOM.span( {className:"caret"})) : this.props.children
        )),
        this.props.dropdown ? this.props.children.slice(1) : null
      )
    );
  },

  handleKeyDown: function(e) {
    if (e.which === 32 && this.state.focused) {
      this.setDropdownState(true);
    }
  },

  handleFocus: function() {
    this.setState({focused: true});
  },

  handleBlur: function() {
    this.setState({focused: false});
  },

  handleOpenClick: function () {
    this.setDropdownState(true);
  },

  handleClick: function (e) {
    if (this.props.dropdown) {
      e.preventDefault();
      this.handleOpenClick();
    } else if (this.props.onSelect) {
      e.preventDefault();

      if (!this.props.disabled) {
        this.props.onSelect(this.props.key,this.props.href);
      }
    }
  }
});

exports["default"] = NavItem;