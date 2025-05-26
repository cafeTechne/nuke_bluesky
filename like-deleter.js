(async function() {
  const SCROLL_DELAY = 3000; // 3 seconds between scrolls
  const CLICK_DELAY = 800;   // 0.8 second between unlikes
  const MAX_SCROLLS = 30;    // Number of scrolls (increase as needed)

  let totalUnliked = 0;
  let lastScrollHeight = 0;
  let scrollCount = 0;

  console.log("Starting de-liker with scrolling...");

  while (scrollCount < MAX_SCROLLS) {
      const unlikeButtons = document.querySelectorAll('button[data-testid="likeBtn"]');
      console.log(`Found ${unlikeButtons.length} like buttons on scroll ${scrollCount + 1}.`);

      let count = 0;
      for (let button of unlikeButtons) {
          if (button.querySelector('svg path[fill="#ec4899"]')) {
              try {
                  button.click();
                  totalUnliked++;
                  count++;
                  console.log(`Unliked post ${count} on this scroll. Total unliked: ${totalUnliked}`);
                  await new Promise(resolve => setTimeout(resolve, CLICK_DELAY));
              } catch (e) {
                  console.warn("Error clicking unlike button:", e);
              }
          }
      }

      window.scrollTo(0, document.body.scrollHeight);
      await new Promise(resolve => setTimeout(resolve, SCROLL_DELAY));

      const newScrollHeight = document.body.scrollHeight;
      if (newScrollHeight === lastScrollHeight) {
          console.log("Reached the bottom of the page or no new content loaded.");
          break;
      }
      lastScrollHeight = newScrollHeight;
      scrollCount++;
  }

  console.log(`Finished! Total unliked posts: ${totalUnliked}`);
})();
