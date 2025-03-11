module.exports = function (eleventyConfig) {
  eleventyConfig.addPlugin(require("@11ty/eleventy-upgrade-help"))
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
