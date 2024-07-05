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
      } else if (line.startsWith('# css {')) {
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
    for (let i = lines.indexOf(startLine) + 1; i < lines.length; i++) {
      const line = lines[i];
      if (line.trim() === '</main>') {
        inMain = false;
        break;
      }
      const element = this.parseElement(line);
      if (element) {
        pageContent.push(element);
      }
    }
    return pageContent;
  }

  parseElement(line) {
    if (line.startsWith('#')) {
      const [type, content] = line.split('{');
      const properties = {};
      const parts = content.split(',');
      for (const part of parts) {
        const [key, value] = part.split(':');
        properties[key.trim()] = value.trim();
      }
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
        } else {
          elementNode.style[key] = value;
        }
      }
      pageWrapper.appendChild(elementNode);
    }

    return pageWrapper;
  }
}

// 使用示例
const wCode = `
#page-title: My Web Page;

# css {
  body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
  }
}

<main>
  #text {
    size: h1,
    content: "This is a heading"
  };
  #button {
    size: auto,
    content: "Click me",
    hover: {{ onClick= () => { alert('clicked'); } }}
  };
  #form {
    size: auto,
    action: {
      url: "/submit",
      method: "post"
    },
    #add-tag {
      type: "text",
      placeholder: "Enter text",
      id: "input-field",
      name: "input-name",
      content: "Default value"
    }
  };
</main>
`;
/*
const interpreter = new WInterpreter();
interpreter.parseW(wCode);
const pageWrapper = interpreter.renderPage();
document.body.appendChild(pageWrapper);
*/
