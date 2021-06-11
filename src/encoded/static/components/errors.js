import React from 'react';
import PropTypes from 'prop-types';
import * as globals from './globals';


const Error = (props) => {
    const context = props.context;
    const itemClass = globals.itemClass(context, 'panel-gray');
    return (
        <div className={itemClass}>
            <h1>{context.title}</h1>
            <p>{context.description}</p>
        </div>
    );
};

Error.propTypes = {
    context: PropTypes.object.isRequired,
};

globals.contentViews.register(Error, 'Error');


const HTTPNotFound = (props) => {
    const context = props.context;
    const itemClass = globals.itemClass(context, 'panel-gray');
    return (
        <div className={itemClass}>
            <h1>Not found</h1>
            <p>The page could not be found. Please check the URL or enter a search term like <em>skin</em>, <em>ChIP-seq</em>, or <em>CTCF</em> in the toolbar above.</p>
        </div>
    );
};

HTTPNotFound.propTypes = {
    context: PropTypes.object.isRequired,
};

globals.contentViews.register(HTTPNotFound, 'HTTPNotFound');


/* eslint-disable react/prefer-stateless-function */
class HTTPForbidden extends React.Component {
    render() {
        const context = this.props.context;
        const itemClass = globals.itemClass(context, 'panel-gray');
        const loggedIn = this.context.session && this.context.session['auth.userid'];
        return (
            <div className={itemClass}>
                <h1>Not available</h1>
                {loggedIn ? <p>Your account is not allowed to view this page.</p> : <p>Please sign in to view this page.</p>}
                {loggedIn ? null : <p> Users of any data provided by KCE agree not to attempt to reidentify any individual participant in any study represented by KCE data,
                    for any purpose whatever. This includes, but is not limited to, the use of analytical techniques of reidentification on genomic or clinical data.</p>}
                {loggedIn ? null : <p>Or <a href="mailto:kce@UTSouthwestern.edu">Request an account.</a></p>}

            </div>
        );
    }
}
/* eslint-enable react/prefer-stateless-function */


HTTPForbidden.propTypes = {
    context: PropTypes.object.isRequired,
};

HTTPForbidden.contextTypes = {
    session: PropTypes.object,
};

globals.contentViews.register(HTTPForbidden, 'HTTPForbidden');


const LoginDenied = (props) => {
    const context = props.context;
    const itemClass = globals.itemClass(context, 'panel-gray');
    return (
        <div className={itemClass}>
            <h2>Our Apologies!</h2>
            <p>The email address you have provided us does not match any user in the Portal.</p>
            <p>
                The KCE Portal uses a your UT Southwestern email to verify you are who say you are.<br />
                The email address you use as your &ldquo;id&rdquo; must match exactly the email address in our system.
            </p>

            <p>Please be aware that full download access is only avaiable to those that agree to all terms and conditions.</p>
            <p> Users of any data provided by KCE agree not to attempt to reidentify any individual participant in any study represented by KCE data,
                for any purpose whatever. This includes, but is not limited to, the use of analytical techniques of reidentification on genomic or clinical data.</p>
            <p>Please contact <a href="mailto:kce@UTSouthwestern.edu">Help Desk</a> if you need an account</p>
            <p><a href="https://www.utsouthwestern.edu/legal/privacy-policy.html">Privacy Policy</a></p>
        </div>
    );
};

LoginDenied.propTypes = {
    context: PropTypes.object.isRequired,
};

globals.contentViews.register(LoginDenied, 'LoginDenied');


const RenderingError = (props) => {
    const context = props.context;
    const itemClass = globals.itemClass(context, 'panel-gray');
    return (
        <div className={itemClass}>
            <h1>{context.title}</h1>
            <p>{context.description}</p>
            <pre>{context.detail}</pre>
        </div>
    );
};

RenderingError.propTypes = {
    context: PropTypes.object.isRequired,
};

globals.contentViews.register(RenderingError, 'RenderingError');
