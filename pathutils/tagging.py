import os.path, hashlib

from . import relative, expand, add_sep

def sum_filename(filename):
    m = hashlib.md5()
    m.update(filename)
    ext = os.path.splitext(filename)[1]
    return m.hexdigest() + ext


class PathTags(object):

    def __init__(self, directory):
        self.directory = expand(directory)
        self.load()

    def _get_basenames(self, directory):
        names = {}
        for root, dirs, files in os.walk(directory):
            if root == self.directory: continue
            names.update(dict(((f, os.path.join(root, f)) for f in files)))
        return names

    def get_tags(self, filename=None):
        if filename: return self.tags.get(expand(filename), [])
        return sorted(set(sum(self.tags.values(), [])))

    def set_tags(self, filename, tags):
        fn = expand(filename)
        if tags:
            self.tags[fn] = sorted(set(tags))
        elif fn in self.tags:
            del(self.tags[fn])

    def add_tags(self, filename, tags):
        fn = expand(filename)
        self.set_tags(fn, self.get_tags(fn) + tags)

    def remove_tags(self, filename, tags):
        fn = expand(filename)
        self.set_tags(fn, list(set(self.get_tags(fn)) - set(tags)))

    def get_paths(self, tags=None):
        return sorted(fn for fn, t in self.tags.items() if all([i in t for i in tags]))

    def repair(self, directory):
        pool = self._get_basenames(directory)
        delete = []
        update = {}
        for path, tags in self.tags.iteritems():
            if os.path.exists(path): continue
            fn = os.path.basename(path)
            delete.append(path)
            if fn not in pool: continue
            update[pool[fn]] = tags
        for path in delete:
            del(self.tags[path])
        self.tags.update(update)

    def write(self):
        # Remove items that have no tags
        self.tags = dict((k, v) for k, v in self.tags.iteritems() if v)
        for fn, tags in self.old_tags.iteritems():
            sumfn = sum_filename(fn)
            if fn in self.tags and self.tags[fn]: continue
            for tag in tags:
                d = os.path.join(self.directory, tag)
                if not os.path.isdir(d): continue
                link = os.path.join(d, sumfn)
                if os.path.islink(link):
                    os.remove(link)
        for fn, tags in self.tags.iteritems():
            sumfn = sum_filename(fn)
            # Get rid of the tags that no longer exist
            for tag in set(self.old_tags.get(fn, [])) - set(tags):
                d = os.path.join(self.directory, tag)
                if not os.path.isdir(d): continue
                link = os.path.join(d, sumfn)
                if os.path.islink(link):
                    os.remove(link)
            # Store the current tags
            for tag in tags:
                d = os.path.join(self.directory, tag)
                if not os.path.isdir(d): os.makedirs(d)
                link = os.path.join(d, sumfn)
                if os.path.exists(fn) and not os.path.exists(link):
                    rel_fn = os.path.join(relative(os.path.dirname(fn), d), os.path.basename(fn))
                    os.symlink(rel_fn, link)
        self.old_tags = self.tags.copy()

    def load(self):
        self.tags = {}
        self.old_tags = {}
        if not os.path.isdir(self.directory): return
        for tag in os.listdir(self.directory):
            directory = os.path.join(self.directory, tag)
            if not os.path.isdir(directory): continue
            for sumfn in os.listdir(directory):
                fn = os.path.join(directory, sumfn)
                if not os.path.islink(fn): continue
                fn = os.path.normpath(os.path.join(directory, os.readlink(fn)))
                self.add_tags(fn, [tag])
        self.old_tags.update(self.tags)
