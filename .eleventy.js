module.exports = function (eleventyConfig) {
  return {
    dir: {
      input: "./source",
      // look in source/templates instead of _include for layouts and other includes
      includes: "static",
      layouts: "templates",
    },
    templateFormats: ["md", "html", "liquid", "png"],
  };
};
