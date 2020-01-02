function util__is_valid(value) {
  var re;
  re = /^[a-zA-Z][a-zA-Z0-9\-_]+$/;
  return value && re.test(value);
};

function util__bound(element) {
    var bound, rect, scrollLeft, scrollTop;
    scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    scrollLeft = document.documentElement.scrollLeft || document.body.scrollLeft;
    rect = element.getBoundingClientRect();
    bound = {
      width: rect.width,
      height: rect.height,
      left: rect.left + scrollLeft,
      top: rect.top + scrollTop
    };
    return bound;
  };

function util__computed(element) {
  var computed, data, defaults, key, _i, _len;
  defaults = document.defaultView.getComputedStyle(document.body);
  computed = document.defaultView.getComputedStyle(element);
  data = {};
  for (_i = 0, _len = computed.length; _i < _len; _i++) {
    key = computed[_i];
    if (key === 'width' || key === 'height' || key === 'top' || key === 'left' || key === 'right' || key === 'bottom') {
      continue;
    }
    if (key.charAt(0) === '-') {
      continue;
    }
    if (computed[key] === defaults[key]) {
      continue;
    }
    data[key] = computed[key];
  }
  return data;
};

// Extractors //////////////////////////////////////////////////////////////////////////

function extractor__extract_meta() {
  var data, meta_tags, titles;

  titles = (function () {
    var _i, _len, _ref, _results;
    _ref = document.querySelectorAll('title');
    _results = [];
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      title = _ref[_i];
      _results.push(title.innerText);
    }
    return _results;
  })();

  meta_tags = (function () {
    var _i, _len, _ref, _results;

    _results = {}
    _meta_tags = document.getElementsByTagName('meta');

    for (_i=0, _len=_meta_tags.length; _i<_len; _i++) {
      _ref = _meta_tags[_i].attributes
      if (_ref.length > 1) {
        _kval = _ref[0].value
        if (_kval in _results) {
          _results[_kval + '_' + _i] = _ref[1].value
        } else {
          _results[_kval] = _ref[1].value
        };
      };
    };
    return _results;
  })();

  data = {
    url: window.location.href,
    titles: titles,
    meta_tags: meta_tags
  };
  return data;
};


function extractor__extract_body () {
  var body, computed, key, _i, _len, _ref;
  computed = {};
  _ref = document.defaultView.getComputedStyle(document.body);
  for (_i = 0, _len = _ref.length; _i < _len; _i++) {
    key = _ref[_i];
    if (key.charAt(0) === '-') {
      continue;
    }
    computed[key] = document.defaultView.getComputedStyle(document.body)[key];
  }
  body = {
    scroll: {
      top: document.documentElement.scrollTop || document.body.scrollTop,
      left: document.documentElement.scrollLeft || document.body.scrollLeft
    },
    bound: util__bound(document.body),
    computed: computed
  };
  return body;
};

function extractor__extract_texts() {
  var bound, computed, node, text, texts, walker;
  texts = [];
  walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
  while (text = walker.nextNode()) {
    if (!(text.nodeValue.trim().length > 0)) {
      continue;
    }
    node = text.parentElement;
    bound = util__bound(node);
    if (!(bound.width * bound.height > 0)) {
      continue;
    }
    while (node) {
      computed = document.defaultView.getComputedStyle(node);
      if (parseInt(computed.width) * parseInt(computed.height) > 0) {
        break;
      }
      node = node.parentElement;
    }
    if (!node) {
      continue;
    }
    if (node.__spider) {
      node.__spider.text.push(text.nodeValue);
      continue
    }
    node.__spider = {
      selector: util__path(node),
      text: [text.nodeValue],
      html: node.innerHTML,
      bound: util__bound(node),
      computed: util__computed(node)
    };
    texts.push(node.__spider);
    node.style.border = '1px solid red';
  }
  return texts;
};

function extractor__extract_links() {
  var link, _i, _len, _ref, _results;
  _ref = document.querySelectorAll('a[href]');
  _results = [];
  for (_i = 0, _len = _ref.length; _i < _len; _i++) {
    link = _ref[_i];
    _results.push(link.href);
  }
  return _results
};

function extractor__extract_images() {
  var bound, images, node, _i, _len, _ref;
  images = [];
  _ref = document.querySelectorAll('img[src]');
  for (_i = 0, _len = _ref.length; _i < _len; _i++) {
    node = _ref[_i];
    bound = util__bound(node);
    if (!(bound.width * bound.height > 0)) {
      continue;
    }
    images.push({
      src: node.src,
      selector: util__path(node),
      bound: bound,
      computed: util__computed(node)
    });
  }
  return images;
};

function extract() {
  var data
  data = extractor__extract_meta();
  data['links'] = extractor__extract_links();
  data['body'] = extractor__extract_body();
  data['texts'] = extractor__extract_texts();
  data['images'] = extractor__extract_images();
  return data
};

return extract();