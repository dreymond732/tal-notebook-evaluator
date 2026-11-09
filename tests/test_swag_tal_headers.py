"""Contrat statique : la conf TAL ne redéfinit pas les headers du proxy SWAG."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SWAG_TAL = ROOT / "deploy" / "swag" / "universite-tal.subfolder.conf"


class SwagTalHeaderTests(unittest.TestCase):
    def test_no_duplicate_headers_defined_by_base_proxy_conf(self):
        source = SWAG_TAL.read_text(encoding="utf-8")
        active = "\n".join(line.partition("#")[0] for line in source.splitlines())
        headers = re.findall(r"^\s*proxy_set_header\s+([^\s;]+)", active, re.M)
        self.assertEqual(headers, ["X-Forwarded-Prefix", "X-Script-Name"])
        for common in ("Host", "X-Forwarded-Host", "X-Forwarded-Proto"):
            self.assertNotIn(common, headers)

    def test_proxy_rewrite_and_target_unchanged(self):
        source = SWAG_TAL.read_text(encoding="utf-8")
        for item in (
            "include /config/nginx/proxy.conf;",
            "include /config/nginx/resolver.conf;",
            "set $upstream_app corrector-tal;",
            "set $upstream_port 5001;",
            "rewrite ^/universite/tal(/.*)$ $1 break;",
            "proxy_pass $upstream_proto://$upstream_app:$upstream_port;",
        ):
            self.assertIn(item, source)


if __name__ == "__main__":
    unittest.main()
