#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import importlib
import time
import warnings
from typing import Any

from flask import Flask, g, redirect, request, session
from flask_topassets import TopAssets
from toppath.path import Path
from wtforms import HiddenField

__version__ = "1.4.0.20250920"

CATEGORY_MAPS = dict(warn="warning", error="danger", important="danger")
FLASH_ICON_MAPS = dict(
    success="check",
    primary="check",
    secondary="check",
    info="info-circle",
    warn="exclamation-circle",
    warning="exclamation-circle",
    error="circle-x",
    danger="circle-x",
    question="help",
)
FLASH_ICON_COLOR_MAPS = dict(warn="warning", error="red", danger="red", question="info")

IMAGE_EXTS = (
    ".apng",
    ".png",
    ".jpg",
    ".avif",
    ".gif",
    ".jpg",
    ".jpeg",
    ".jfif",
    ".pjepg",
    ".pjp",
    ".svg",
    ".webp",
)
LAYOUTS = [
    "boxed",
    "combined",
    "condensed",
    "condensed-box",
    "fluid",
    "fluid-vertical",
    "horizontal",
    "navbar-dark",
    "fluid-navbar-dark",
    "overlap",
    "fluid-overlap",
    "transparent",
    "vertical-right",
    "vertical",
]


def is_hidden_field_filter(field: Any) -> bool:
    return isinstance(field, HiddenField)


def raise_helper(message: Any):  # pragma: no cover
    raise RuntimeError(message)


def fake_trans(text: Any, *args: Any, **kwargs: Any) -> str:
    return f"{text}"


def merge_dict(left: dict, right: Any, fallback: dict = {}) -> dict:
    return dict(left, **(right or fallback))


def is_image_url(path: str) -> bool:
    p = path.strip().lower()
    return p.lower().endswith(IMAGE_EXTS) or p.startswith("data:image")


class Tabler(TopAssets):
    def __init__(self, app: Flask | None = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        self.prepare(app, register=False)

        app.jinja_env.globals["_"] = fake_trans  # fake translation function
        app.jinja_env.globals["merge_dict"] = merge_dict
        app.jinja_env.globals["warn"] = warnings.warn
        app.jinja_env.globals["raise"] = raise_helper
        app.jinja_env.globals["is_hidden_field"] = is_hidden_field_filter
        # app.jinja_env.trim_blocks = True
        # app.jinja_env.lstrip_blocks = True

        app.jinja_env.add_extension("jinja2.ext.do")
        app.jinja_env.tests["image_data"] = is_image_url
        # default settings
        app.config.setdefault("TABLER_SERVE_LOCAL", True)
        app.config.setdefault("TABLER_BTN_STYLE", "primary")
        app.config.setdefault("TABLER_BTN_SIZE", "md")
        app.config.setdefault("TABLER_ICON_SIZE", 24)
        app.config.setdefault("TABLER_ICON_COLOR", "blue")
        app.config.setdefault("TABLER_MSG_CATEGORY", "primary")
        app.config.setdefault("TABLER_VIEW_TITLE", "View")
        app.config.setdefault("TABLER_EDIT_TITLE", "Edit")
        app.config.setdefault("TABLER_DELETE_TITLE", "Delete")
        app.config.setdefault("TABLER_NEW_TITLE", "New")
        app.config.setdefault("TABLER_FORM_GROUP_CLASSES", "mb-3")
        app.config.setdefault("TABLER_LAYOUT", "boxed")
        app.config.setdefault("TABLER_ENABLE_LAYOUT_CHOICE", True)
        app.config.setdefault("TABLER_STICKY_TOP", True)
        app.config.setdefault("TABLER_THEME_DARK_MODE", False)
        app.config.setdefault("TABLER_ENABLE_THEME_MODE", True)
        app.config.setdefault("TABLER_LAYOUTS", LAYOUTS)
        app.config.setdefault("TABLER_ENABLE_I18N", True)
        app.config.setdefault("TABLER_SHOW_HEADER_SEARCH", True)
        app.config.setdefault("TABLER_LANGUAGE", "zh")
        app.config.setdefault("TABLER_LANGUAGES", [("zh", "cn", "中文"), ("en", "us", "English")])

        # tabler 1.2.0 additional settings
        app.config.setdefault("TABLER_THEME_RADIUS", 1)
        app.config.setdefault("TABLER_THEME_BASE", "gray")
        app.config.setdefault("TABLER_THEME_PRIMARY", "blue")
        app.config.setdefault("TABLER_THEME_FONT", "sans-serif")

        # html uses alert element, js uses sweetalert2 to popup
        # app.config.setdefault("TABLER_FLASHES_TYPE", "js")
        app.config.setdefault("TABLER_FLASHES_TYPE", "html")

        # plugins, move vendors outside of tabler as plugins
        app.config.setdefault("TABLER_PLUGINS", [])

        # add default plugins
        plugins = app.config["TABLER_PLUGINS"]
        plugins.append("tomselect")
        plugins.append("sweetalert2")
        plugins.insert(0, "tabler")
        plugins.insert(0, "autosize")

        # move countup to first if enabled
        if "countup" in plugins:
            plugins.remove("countup")
            plugins.insert(0, "countup")

        mods = dict(tabler=self)
        # prepare plugins for template
        for plugin in plugins:
            if plugin not in mods:
                mod = importlib.import_module(f"flask_{plugin}")
                mod_name = getattr(mod, "CLASS_NAME")
                obj = getattr(mod, mod_name)(app)
                mods[plugin] = obj

        app.config["TABLER_PLUGINS_MODULES"] = mods
        self.setup_routes(app)
        app.register_blueprint(self.bp)

        self.setup_filters(app)
        self.bundle_js(
            ["js/jquery.min.js", "js/jquery.mark.min.js", "js/tabler.min.js"], output="js/packed.js"
        )
        self.bundle_js(
            "js/website.js",
            key="other_js",
            filters="jsmin",
            output="js/packed_others.js",
        )
        self.bundle_css(
            [
                "css/tabler.min.css",
                "css/tabler-flags.min.css",
                "css/tabler-props.min.css",
                "css/tabler-themes.min.css",
                "css/tabler-socials.min.css",
                "css/tabler-vendors.min.css",
                "css/tabler-payments.min.css",
            ],
            output="css/packed.css",
        )
        self.bundle_css(
            ["css/inter.css", "css/website.css"],
            key="other_css",
            filters="cssmin",
            output="css/packed_others.css",
        )
        self.get_path("css")
        self.get_path("other_css", "css")
        self.get_path("js")
        self.get_path("other_js", "js")

        self.copy_folder("img")
        self.copy_folder("fonts")

    @classmethod
    def get_lang(cls, app: Flask) -> str:
        if lang := app.config.get("TABLER_LANGUAGE"):
            return lang

        try:
            return request.accept_languages.best.split("-")[0]
        except Exception:
            return "zh"

    def setup_routes(self, app: Flask) -> None:
        @app.before_request
        def load_configs() -> None:
            if request.endpoint != "static":
                if app.config.get("TABLER_SHOW_REQUEST_TIME"):
                    g._start = time.perf_counter() * 1000
                    g._request_time = lambda: f"{(1000 * time.perf_counter() - g._start):.3f}"

                conf_color = app.config.get("TABLER_THEME_COLOR")
                conf_layout = app.config.get("TABLER_LAYOUT")
                conf_dark = app.config.get("TABLER_THEME_DARK_MODE")
                if app.config.get("SECRET_KEY"):
                    color = session.get("theme_color") or conf_color
                    layout = session.get("page_layout") or conf_layout
                    dark_mode = session.get("dark_mode")
                    if dark_mode is None:
                        dark_mode = conf_dark

                    if "page_lang" not in session:
                        session["page_lang"] = self.get_lang(app)

                    g.lang = session["page_lang"]
                else:
                    color = conf_color
                    layout = conf_layout
                    dark_mode = conf_dark
                    g.lang = self.get_lang(app)

                g.tabler_theme_primary = (color or "blue").lower()
                g.tabler_layout = (layout or "boxed").lower()
                g.dark_mode = app.config.get("TABLER_ENABLE_THEME_MODE") and dark_mode

        @self.bp.route("/tabler")
        def index() -> Any:
            if mode := request.args.get("theme"):
                session["dark_mode"] = mode.lower() == "dark"

            if layout := request.args.get("layout"):
                session["page_layout"] = layout.lower()

            if color := request.args.get("theme_color"):
                session["theme_color"] = color.lower()

            if lang := request.args.get("lang"):
                session["page_lang"] = lang.lower()

            return redirect(request.referrer or "/")

    def setup_filters(self, app: Flask) -> None:
        @app.template_filter("get_flash_category")
        def get_flash_category_filter(category: str) -> str:
            return CATEGORY_MAPS.get(category, category)

        @app.template_filter("get_flash_icon")
        def get_flash_icon_filter(category: str) -> str:
            return FLASH_ICON_MAPS.get(category) or "check"

        @app.template_filter("get_flash_icon_kw")
        def get_flash_icon_kw(category: str) -> dict:
            return dict(size=26, color=FLASH_ICON_COLOR_MAPS.get(category) or category)

    def copy_folder(self, folder: str = "fonts") -> None:
        targets = {}
        src = Path(self.bp.static_folder) / folder
        dst = Path(self.app.static_folder) / "gen/tabler" / folder
        for fp in src.walkfiles():
            dest = dst / fp.relpath(src)
            targets.setdefault(dest.dirname(), [])
            targets[dest.dirname()].append((dest, fp))

        for dest, files in targets.items():
            dest.makedirs_p()
            for f, src_fp in files:
                to = dest / f
                if not (to.exists() and to.is_same(f)):
                    src_fp.copy2(to)
