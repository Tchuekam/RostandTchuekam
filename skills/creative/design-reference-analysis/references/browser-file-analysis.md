# Browser-Based Local File Analysis

## Using `file:///` Protocol

On Windows, local images can be opened in the browser tool using:

```
file:///C:/Users/USERNAME/Path/To/Image%20with%20spaces.jpg
```

### Behavior Notes

- **No interactive elements**: Local image files render as `<img>` in an empty HTML page. No ref IDs will appear in snapshots.
- **Extract info via**: `browser_console(expression="document.querySelector('img').naturalWidth")` for dimensions
- **Protocol works in**: The browser tool supports `file:///` URIs — but only for file types the browser can render (images, PDFs, HTML files).

### Spaced Filenames

Windows paths with spaces need `%20` encoding:
- Wrong: `file:///C:/Users/CLINIC/Documents/My File.jpg`
- Right: `file:///C:/Users/CLINIC/Documents/My%20File.jpg`

Special characters (é, à, ö, etc.) and emoji in filenames may fail to render in browser. Use the filesystem tools (ls, search_files) for accurate info instead.
