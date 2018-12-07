# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import sys
import re


def resolveSyntaxType(view):

    syntax = view.settings().get('syntax')
    fileSuffix = ""
    if syntax == "Packages/JavaScript/JSON.sublime-syntax":
        fileSuffix = "json"
    elif syntax == "Packages/JavaScript/JavaScript.sublime-syntax":
        fileSuffix = "js"
    elif syntax == "Packages/CSS/CSS.sublime-syntax":
        fileSuffix = "css"

    print(syntax)
    return fileSuffix


class ChineseCharactersToUnicodeCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        fileSuffix = resolveSyntaxType(self.view)
        if fileSuffix == "js" or fileSuffix == "json" or fileSuffix == "css":
            def TU(x):
                if fileSuffix == "js" or fileSuffix == "json":
                    return '\\u'+('000'+hex(ord(x))[2:])[-4:]
                else:
                    return '\\'+('000'+hex(ord(x))[2:])[-4:]

            def toUnicode(x):
                s = x.group(0)
                s = list(s)
                mapValue = map(TU, s)
                s = "".join(mapValue)
                return s
            regions = self.view.sel()
            if not regions[0].empty():
                for region in regions:
                    if not region.empty():
                        s = self.view.substr(region)
                        s = re.sub(r"([\u4e00-\u9fa5]+)", toUnicode, s)
                        self.view.replace(edit, region, s)
            else:
                region = sublime.Region(0, self.view.size())
                s = self.view.substr(region)
                s = re.sub(r"([\u4e00-\u9fa5]+)", toUnicode, s)

                self.view.replace(edit, region, s)
        else:
            sublime.error_message('ConvertChineseCharacters allowing you to convert your .js, .json, and .css files')


class UnicodeToChineseCharactersCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        fileSuffix = resolveSyntaxType(self.view)

        if fileSuffix == "js" or fileSuffix == "json" or fileSuffix == "css":
            def unicodeTo(x):
                s = x.group(0)
                if fileSuffix == "js" or fileSuffix == "json":
                    s = s[2:]
                else:
                    s = s[1:]
                s = chr(int(s, 16))
                return s
            regions = self.view.sel()
            if not regions[0].empty():
                for region in regions:
                    if not region.empty():
                        s = self.view.substr(region)
                        if fileSuffix == "js" or fileSuffix == "json":
                            s = re.sub(r"(\\[uU]\w{4})", unicodeTo, s)
                        else:
                            s = re.sub(r"(\\\w{4})", unicodeTo, s)
                        self.view.replace(edit, region, s)
            else:
                region = sublime.Region(0, self.view.size())
                s = self.view.substr(region)
                if fileSuffix == "js" or fileSuffix == "json":
                    s = re.sub(r"(\\[uU]\w{4})", unicodeTo, s)
                else:
                    s = re.sub(r"(\\\w{4})", unicodeTo, s)
                self.view.replace(edit, region, s)
        else:
            sublime.error_message('ConvertChineseCharacters allowing you to convert your .js, .json, and .css files')
