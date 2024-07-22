class WInterpreter {
  constructor() {
    this.pageTitle = '';
    this.cssCode = '';
    this.pageContent = [];
  }

  parseW(code) {
    const lines = code.split('\n');
    for (const line of lines) {
      if (line.startsWith('#page-title:')) {
        this.pageTitle = line.split(':')[1].trim();
      } else if (line.startsWith('#css {')) {
        this.cssCode = this.parseCss(lines, line);
      } else if (line.startsWith('<main>')) {
        this.pageContent = this.parseMain(lines, line);
      }
    }
  }

  parseCss(lines, startLine) {
    let cssCode = '';
    let inCss = true;
    for (let i = lines.indexOf(startLine) + 1; i < lines.length; i++) {
      const line = lines[i];
      if (line.trim() === '}') {
        inCss = false;
        break;
      }
      cssCode += line + '\n';
    }
    return cssCode;
  }

  parseMain(lines, startLine) {
    const pageContent = [];
    let inMain = true;
    let currentElement = null;
    for (let i = lines.indexOf(startLine) + 1; i < lines.length; i++) {
      const line = lines[i];
      if (line.trim() === '</main>') {
        inMain = false;
        break;
      }
      if (line.startsWith('#')) {
        currentElement = this.parseElement(line);
        pageContent.push(currentElement);
      } else if (line.startsWith('  ') && currentElement) {
        const [key, value] = line.trim().split(':');
        currentElement.properties[key.trim()] = value.trim();
      }
    }
    return pageContent;
  }

  parseElement(line) {
    if (line.startsWith('#')) {
      const [type, content] = line.split('{');
      const properties = {};
      return { type: type.trim(), properties };
    }
  }

  renderPage() {
    const pageWrapper = document.createElement('div');
    const pageTitle = document.createElement('h1');
    pageTitle.textContent = this.pageTitle;
    pageWrapper.appendChild(pageTitle);

    const styleElement = document.createElement('style');
    styleElement.textContent = this.cssCode;
    pageWrapper.appendChild(styleElement);

    for (const element of this.pageContent) {
      const { type, properties } = element;
      const elementNode = document.createElement(type);
      for (const [key, value] of Object.entries(properties)) {
        if (key === 'hover') {
          elementNode.addEventListener('click', new Function(value));
        } else if (key === 'size') {
          const [fontSize, contentValue] = value.split(',');
          elementNode.style.fontSize = fontSize.trim();
          elementNode.textContent = contentValue.trim();
        } else if (key === 'action') {
          const { url, method } = JSON.parse(value);
          elementNode.setAttribute('action', url);
          elementNode.setAttribute('method', method);
        } else {
          elementNode.style[key] = value;
        }
      }
      pageWrapper.appendChild(elementNode);
    }

    return pageWrapper;
  }
}
