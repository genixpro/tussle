import React from 'react';


// Use a class component to hook into life-cycle componentDidCatch
class ErrorBoundary extends React.Component {
    state = {}

    componentDidCatch(error, info) {
        localStorage.removeItem('chart-default');
        localStorage.removeItem('chart-list-state');
    }

    render() {
        return this.props.children;
    }
}

export default ErrorBoundary;

