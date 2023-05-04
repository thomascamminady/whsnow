from typing import Union


def centered_markdown_title(
    text: str,
    href: Union[str, None] = None,
    heading_level: int = 1,
) -> str:
    if href is None:
        return f"""<h{heading_level} style='text-align: center; color: grey;'>{text}</h{heading_level}>"""
    else:
        return f"""<h{heading_level} style='text-align: center; color: grey;'><a href={href} style='text-decoration: none; color: inherit;'>{text}</a></h{heading_level}>"""
