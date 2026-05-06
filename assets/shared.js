/**
 * Rodgers Playbook — shared schema helpers (v2 blocks model).
 * Viewer and Editor both load this file. Blocks are the source of truth for slide body content.
 */
(function (global) {
  'use strict';

  var SCHEMA_VERSION = 2;

  function newBlockId() {
    return 'b_' + Math.random().toString(36).slice(2, 9);
  }

  function escapeHtml(s) {
    return String(s || '').replace(/[&<>"']/g, function (m) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[m];
    });
  }

  var PAIRING_LABELS = {
    'real-vs-cad': 'Real-world + CAD',
    'existing-vs-finished': 'Existing + Finished',
    'diagram-vs-field': 'Diagram + Field',
    'plan-vs-section': 'Plan + Section',
    'construction-vs-final': 'Construction + Final',
    'good-vs-bad': 'Good + Bad Example',
    custom: 'Custom',
  };

  var PAIRING_TAG_CLASS = {
    'real-vs-cad': 'amber',
    'existing-vs-finished': 'green',
    'diagram-vs-field': 'gold',
    'plan-vs-section': '',
    'construction-vs-final': 'amber',
    'good-vs-bad': 'green',
    custom: '',
  };

  var TEACHING_QUESTIONS = [
    'What are we looking at?',
    'What is the relationship between the two?',
    'Why does it matter on a project?',
    'What should an intern notice?',
    'Takeaway',
  ];

  function defaultImages() {
    return [
      { src: null, label: '', type: 'Real-world photo' },
      { src: null, label: '', type: 'CAD plan view' },
    ];
  }

  function makeImagePairBlock(layout) {
    return {
      id: newBlockId(),
      type: 'imagePair',
      layout: layout || 'two',
      images: defaultImages(),
    };
  }

  function makeTeachingBlock(t) {
    t = t || {};
    return {
      id: newBlockId(),
      type: 'teaching',
      t1: t.t1 || '',
      t2: t.t2 || '',
      t3: t.t3 || '',
      t4: t.t4 || '',
      t5: t.t5 || '',
    };
  }

  function makeKeyLessonBlock(text) {
    return { id: newBlockId(), type: 'keyLesson', text: text || '' };
  }

  function makeDefaultSlideBlocks() {
    return [makeImagePairBlock('two'), makeKeyLessonBlock(''), makeTeachingBlock({})];
  }

  function stripLegacySlideFields(slide) {
    delete slide.images;
    delete slide.keyLesson;
    delete slide.teaching;
    delete slide.imageLayout;
  }

  function ensureBlockIds(slide) {
    (slide.blocks || []).forEach(function (b) {
      if (!b.id) b.id = newBlockId();
    });
  }

  /** @returns {{ images: [{src,label,type},{src,label,type}], layout: string } | null } */
  function getImagePair(slide) {
    var block = getImagePairBlock(slide);
    if (!block) return null;
    return {
      layout: block.layout || 'two',
      images: block.images && block.images.length
        ? block.images
        : defaultImages(),
    };
  }

  function getImagePairBlock(slide) {
    if (!slide.blocks) return null;
    for (var i = 0; i < slide.blocks.length; i++) {
      if (slide.blocks[i].type === 'imagePair') return slide.blocks[i];
    }
    return null;
  }

  function getKeyLessonBlock(slide) {
    if (!slide.blocks) return null;
    for (var j = 0; j < slide.blocks.length; j++) {
      if (slide.blocks[j].type === 'keyLesson') return slide.blocks[j];
    }
    return null;
  }

  function getTeachingBlock(slide) {
    if (!slide.blocks) return null;
    for (var k = 0; k < slide.blocks.length; k++) {
      if (slide.blocks[k].type === 'teaching') return slide.blocks[k];
    }
    return null;
  }

  /** Key lesson plain text from blocks only */
  function getKeyLessonText(slide) {
    var b = getKeyLessonBlock(slide);
    return (b && b.text) ? String(b.text).trim() : '';
  }

  /** Teaching scaffold t1–t5 from blocks */
  function getTeachingMap(slide) {
    var b = getTeachingBlock(slide);
    if (!b) return { t1: '', t2: '', t3: '', t4: '', t5: '' };
    return {
      t1: b.t1 || '',
      t2: b.t2 || '',
      t3: b.t3 || '',
      t4: b.t4 || '',
      t5: b.t5 || '',
    };
  }

  function slideHasLegacyBody(slide) {
    return !!(slide.images && slide.images.length);
  }

  function migrateSlideV1ToV2(slide) {
    var images = JSON.parse(
      JSON.stringify(
        slide.images && slide.images.length >= 2
          ? slide.images
          : defaultImages()
      )
    );
    var layout = slide.imageLayout || 'two';
    var blocks = [];
    blocks.push({
      id: newBlockId(),
      type: 'imagePair',
      layout: layout === 'one' ? 'one' : 'two',
      images: images,
    });
    var kl = (slide.keyLesson || '').trim();
    if (kl) blocks.push(makeKeyLessonBlock(slide.keyLesson));
    blocks.push(makeTeachingBlock(slide.teaching || {}));

    return {
      id: slide.id,
      title: slide.title || 'Slide',
      subtitle: slide.subtitle || '',
      pairing: slide.pairing || 'real-vs-cad',
      level: slide.level != null ? slide.level : 1,
      status: slide.status || 'draft',
      tags: slide.tags || '',
      narration: slide.narration || {
        audio: null,
        mime: null,
        duration: 0,
        script: '',
      },
      annotations: slide.annotations || [],
      speakerNotes: slide.speakerNotes || '',
      projectContext: slide.projectContext || '',
      resources: slide.resources || '',
      imageLayout:
        slide.imageLayout ||
        blocks[0].layout /* compat for external readers */,
      blocks: blocks,
    };
  }

  /**
   * Normalize a single slide to v2: blocks populated, legacy body fields removed.
   */
  function normalizeSlide(slide) {
    if (!slide.blocks || !slide.blocks.length) {
      if (slideHasLegacyBody(slide) || slide.keyLesson !== undefined || slide.teaching !== undefined) {
        return migrateSlideV1ToV2(slide);
      }
      var copy = {};
      Object.keys(slide).forEach(function (key) {
        copy[key] = slide[key];
      });
      copy.blocks = makeDefaultSlideBlocks();
      stripLegacySlideFields(copy);
      copy.imageLayout = getImagePairBlock(copy).layout;
      ensureBlockIds(copy);
      return copy;
    }
    stripLegacySlideFields(slide);
    ensureBlockIds(slide);
    var pair = getImagePairBlock(slide);
    slide.imageLayout = pair ? pair.layout : 'two';
    return slide;
  }

  /**
   * Deep-clone library and migrate to schema v2 in memory (JSON-safe structure).
   */
  function migrateLibrary(lib) {
    var out = JSON.parse(JSON.stringify(lib));
    var ver = out.version || 1;
    out.version = SCHEMA_VERSION;
    out.modules.forEach(function (mod) {
      mod.slides = mod.slides.map(function (s) {
        if (ver >= 2 && Array.isArray(s.blocks) && s.blocks.length > 0) {
          stripLegacySlideFields(s);
          ensureBlockIds(s);
          var p = getImagePairBlock(s);
          s.imageLayout = p ? p.layout : 'two';
          return s;
        }
        if (Array.isArray(s.blocks) && s.blocks.length === 0) {
          delete s.blocks;
        }
        return migrateSlideV1ToV2(s);
      });
    });
    /* Keep imageLayout in sync */
    out.modules.forEach(function (mo) {
      mo.slides.forEach(function (sl) {
        var pr = getImagePairBlock(sl);
        if (pr) sl.imageLayout = pr.layout;
      });
    });
    return out;
  }

  /** Collect searchable text from slide body (blocks + metadata). */
  function slideSearchBlob(slide) {
    var parts = [
      slide.title,
      slide.subtitle,
      slide.tags,
      getKeyLessonText(slide),
      slide.pairing,
    ];
    var pair = getImagePair(slide);
    if (pair && pair.images) {
      pair.images.forEach(function (img) {
        parts.push(img.label, img.type);
      });
    }
    var tm = getTeachingMap(slide);
    parts.push(tm.t1, tm.t2, tm.t3, tm.t4, tm.t5);
    (slide.blocks || []).forEach(function (blk) {
      if (blk.type === 'video' && blk.caption) parts.push(blk.caption);
      if (blk.type === 'richText' && blk.html) parts.push(blk.html);
    });
    return parts.filter(Boolean).join(' ').toLowerCase();
  }

  /** Per-slide: any image slot has src (for module grid). */
  function slideHasAnyImage(slide) {
    var pair = getImagePair(slide);
    if (!pair || !pair.images) return false;
    return pair.images.some(function (im) {
      return !!im.src;
    });
  }

  function slideHasBothImages(slide) {
    var pair = getImagePair(slide);
    if (!pair || !pair.images || pair.images.length < 2) return false;
    if (pair.layout === 'one') return !!pair.images[0].src;
    return !!(pair.images[0].src && pair.images[1].src);
  }

  global.RodgersPlaybookCore = {
    SCHEMA_VERSION: SCHEMA_VERSION,
    newBlockId: newBlockId,
    escapeHtml: escapeHtml,
    PAIRING_LABELS: PAIRING_LABELS,
    PAIRING_TAG_CLASS: PAIRING_TAG_CLASS,
    TEACHING_QUESTIONS: TEACHING_QUESTIONS,
    migrateLibrary: migrateLibrary,
    normalizeSlide: normalizeSlide,
    migrateSlideV1ToV2: migrateSlideV1ToV2,
    getImagePair: getImagePair,
    getImagePairBlock: getImagePairBlock,
    getKeyLessonBlock: getKeyLessonBlock,
    getTeachingBlock: getTeachingBlock,
    getKeyLessonText: getKeyLessonText,
    getTeachingMap: getTeachingMap,
    makeDefaultSlideBlocks: makeDefaultSlideBlocks,
    makeImagePairBlock: makeImagePairBlock,
    makeTeachingBlock: makeTeachingBlock,
    makeKeyLessonBlock: makeKeyLessonBlock,
    stripLegacySlideFields: stripLegacySlideFields,
    slideSearchBlob: slideSearchBlob,
    slideHasAnyImage: slideHasAnyImage,
    slideHasBothImages: slideHasBothImages,
  };
})(typeof window !== 'undefined' ? window : globalThis);
