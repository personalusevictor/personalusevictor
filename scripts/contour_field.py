"""Portable SVG contours from the scalar field used by VCode's homepage."""

import math
from functools import lru_cache
from collections import defaultdict

EDGES = [(0, 1), (1, 2), (2, 3), (3, 0)]
CASES = [
    [],
    [3, 0],
    [0, 1],
    [3, 1],
    [1, 2],
    [3, 2, 0, 1],
    [0, 2],
    [3, 2],
    [2, 3],
    [0, 2],
    [3, 0, 1, 2],
    [1, 2],
    [1, 3],
    [0, 1],
    [3, 0],
    [],
]


def contours(time, level, w=900, h=308):
    scale = max(w / 8, h / 5.2)
    margin = scale * 5.34
    step = max(8, scale / 6.25)
    cols = math.ceil((w + 2 * margin) / step)
    rows = math.ceil((h + 2 * margin) / step)
    xs = [-margin + x * (w + 2 * margin) / cols for x in range(cols + 1)]
    ys = [-margin + y * (h + 2 * margin) / rows for y in range(rows + 1)]
    scale = max(w / 8, h / 5.2)
    us = [(x - w / 2) / scale for x in xs]
    vs = [(y - h / 2) / scale for y in ys]
    data = [
        [
            math.sin(u * 1.55 + math.cos(v * 0.7 + time * 0.17) * 1.1 + time * 0.12)
            + math.sin(v * 1.7 + math.sin(u * 0.8 - time * 0.1) * 0.9 - time * 0.14)
            + math.sin(u * 2.9 + v * 1.4 + time * 0.22) * 0.32
            for u in us
        ]
        for v in vs
    ]
    nodes = {}
    adj = defaultdict(list)
    segments = []

    def vertex(x, y):
        key = round(x, 4), round(y, 4)
        nodes[key] = (x, y)
        return key

    for y in range(rows):
        for x in range(cols):
            values = [data[y][x], data[y][x + 1], data[y + 1][x + 1], data[y + 1][x]]
            code = sum((value > level) << i for i, value in enumerate(values))
            edges = CASES[code]
            if code in (5, 10):
                edges = (
                    [0, 1, 2, 3]
                    if (sum(values) / 4 > level) == (code == 5)
                    else [3, 0, 1, 2]
                )
            points = []
            for edge in edges:
                a, b = EDGES[edge]
                t = (level - values[a]) / (values[b] - values[a])
                ax = 1 if a in (1, 2) else 0
                ay = 1 if a >= 2 else 0
                bx = 1 if b in (1, 2) else 0
                by = 1 if b >= 2 else 0
                points.append(
                    vertex(
                        xs[x] + (ax + (bx - ax) * t) * (xs[x + 1] - xs[x]),
                        ys[y] + (ay + (by - ay) * t) * (ys[y + 1] - ys[y]),
                    )
                )
            for i in range(0, len(points), 2):
                a, b = points[i : i + 2]
                idx = len(segments)
                segments.append((a, b))
                adj[a].append(idx)
                adj[b].append(idx)
    visited = set()
    result = []
    starts = sorted(adj, key=lambda v: len(adj[v]))
    for start in starts:
        for initial in adj[start]:
            if initial in visited:
                continue
            path = [nodes[start]]
            current = start
            edge = initial
            while edge not in visited:
                visited.add(edge)
                a, b = segments[edge]
                current = b if current == a else a
                path.append(nodes[current])
                remaining = [i for i in adj[current] if i not in visited]
                if not remaining:
                    break
                edge = remaining[0]
            if len(path) > 8:
                result.append(path)
    return result


def field_value(x, y, time, width=900, height=308):
    scale = max(width / 8, height / 5.2)
    u = (x - width / 2) / scale
    v = (y - height / 2) / scale
    return (
        math.sin(u * 1.55 + math.cos(v * 0.7 + time * 0.17) * 1.1 + time * 0.12)
        + math.sin(v * 1.7 + math.sin(u * 0.8 - time * 0.1) * 0.9 - time * 0.14)
        + math.sin(u * 2.9 + v * 1.4 + time * 0.22) * 0.32
    )


def center(path):
    return tuple(sum(point[k] for point in path) / len(path) for k in (0, 1))


def sample(path, count=48):
    points = path[:-1] if path[0] == path[-1] else path[:]
    area = sum(
        a[0] * b[1] - b[0] * a[1] for a, b in zip(points, points[1:] + points[:1])
    )
    if area < 0:
        points.reverse()
    segments = list(zip(points, points[1:] + points[:1]))
    lengths = [math.dist(a, b) for a, b in segments]
    total = sum(lengths)
    result = []
    index = 0
    walked = 0
    for n in range(count):
        target = n * total / count
        while index < len(segments) - 1 and walked + lengths[index] < target:
            walked += lengths[index]
            index += 1
        a, b = segments[index]
        t = (target - walked) / max(lengths[index], 1e-9)
        result.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    return result


def align(points, previous):
    def cost(shift):
        return sum(
            math.dist(points[(i + shift) % len(points)], previous[i]) ** 2
            for i in range(0, len(points), 4)
        )

    shift = min(range(len(points)), key=cost)
    return points[shift:] + points[:shift]


def touches(path, width, height):
    xs = [p[0] for p in path]
    ys = [p[1] for p in path]
    return max(xs) >= 0 and min(xs) <= width and max(ys) >= 0 and min(ys) <= height


@lru_cache(maxsize=2)
def tracks(width=900, height=308):
    # Seven field poses are sampled, then returned in reverse to close a smooth loop.
    times = [3 - 3 * math.cos(math.pi * i / 6) for i in range(7)]
    output = []
    for level in (-0.65, 0.65):
        first = [p for p in contours(times[0], level, width, height) if p[0] == p[-1]]
        histories = [[sample(p)] for p in first]
        for time in times[1:]:
            candidates = [
                sample(p) for p in contours(time, level, width, height) if p[0] == p[-1]
            ]
            costs = sorted(
                (math.dist(center(history[-1]), center(candidate)), i, j)
                for i, history in enumerate(histories)
                for j, candidate in enumerate(candidates)
            )
            used_tracks = set()
            used_candidates = set()
            for distance, i, j in costs:
                if i in used_tracks or j in used_candidates:
                    continue
                histories[i].append(align(candidates[j], histories[i][-1]))
                used_tracks.add(i)
                used_candidates.add(j)
            for i, history in enumerate(histories):
                if i not in used_tracks:
                    history.append(history[-1])
        for history in histories:
            if not any(touches(p, width, height) for p in history):
                continue
            max_step = max(
                math.dist(center(a), center(b)) for a, b in zip(history, history[1:])
            )
            if max_step > width * 0.22:
                raise ValueError("A visible contour changed identity during the loop.")
            output.append(history + history[-2::-1])
    return output


def path_data(points):
    """Closed Catmull–Rom spline; fixed command counts allow native SVG morphing."""
    commands = [f"M{points[0][0]:.1f},{points[0][1]:.1f}"]
    count = len(points)
    for i, a in enumerate(points):
        before, b, after = (
            points[(i - 1) % count],
            points[(i + 1) % count],
            points[(i + 2) % count],
        )
        c1 = (a[0] + (b[0] - before[0]) / 6, a[1] + (b[1] - before[1]) / 6)
        c2 = (b[0] - (after[0] - a[0]) / 6, b[1] - (after[1] - a[1]) / 6)
        commands.append(
            f"C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {b[0]:.1f},{b[1]:.1f}"
        )
    return "".join(commands) + "Z"


def easing():
    angles = [math.pi * i / 6 for i in range(13)]
    values = [3 - 3 * math.cos(a) for a in angles]
    delta = math.pi / 6
    out = []
    for i in range(12):
        span = values[i + 1] - values[i]
        a = 3 * math.sin(angles[i]) * delta / (3 * span)
        b = 1 - 3 * math.sin(angles[i + 1]) * delta / (3 * span)
        out.append(f".3333 {max(0,min(1,a)):.4f} .6667 {max(0,min(1,b)):.4f}")
    return ";".join(out)


def backdrop(color, width=900, height=308):
    histories = tracks(width, height)
    key_times = ";".join(f"{i/12:.6f}" for i in range(13))
    result = f'<g fill="none" stroke="{color}" stroke-opacity=".52" stroke-width="1.1" stroke-linejoin="round" stroke-linecap="round">'
    result += '<g class="contour-motion">'
    for history in histories:
        values = ";".join(path_data(p) for p in history)
        result += f'<path d="{path_data(history[0])}"><animate attributeName="d" dur="16s" values="{values}" keyTimes="{key_times}" calcMode="spline" keySplines="{easing()}" repeatCount="indefinite"/></path>'
    result += '</g><g class="contour-static">'
    result += "".join(f'<path d="{path_data(history[0])}"/>' for history in histories)
    return result + "</g></g>"
