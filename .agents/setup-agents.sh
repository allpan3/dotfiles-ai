#!/usr/bin/env bash
set -eo pipefail

warn() {
    printf '\033[33mWarning: %s\033[0m\n' "$*" >&2
}

collect_skills() {
    local directory=$1 child name existing
    if [[ -f "$directory/SKILL.md" ]]; then
        name=${directory##*/}
        for existing in "${names[@]}"; do
            if [[ "$existing" == "$name" ]]; then
                printf 'Duplicate skill folder name: %s\n' "$name" >&2
                return 1
            fi
        done
        names+=("$name")
        paths+=("$directory")
        return
    fi
    for child in "$directory"/*; do
        [[ -d "$child" && ! -L "$child" && ${child##*/} != node_modules ]] || continue
        collect_skills "$child" || return 1
    done
}

link_set() {
    local destination=$1 first=$2 last=$3 target resolved expected i
    mkdir -p -- "$destination"
    for target in "$destination"/*; do
        [[ -L "$target" ]] || continue
        resolved=$(readlink "$target")
        case "$resolved" in
            "$root/skills/"*|"$root/t3/skills/"*) ;;
            *) continue ;;
        esac
        expected=
        for ((i=first; i<last; i++)); do
            [[ ${target##*/} != "${names[$i]}" ]] || expected=${paths[$i]}
        done
        if [[ "$resolved" != "$expected" ]]; then
            rm -- "$target"
            printf 'Removed stale link: %s\n' "$target"
        fi
    done
    for ((i=first; i<last; i++)); do
        target=$destination/${names[$i]}
        if [[ -L "$target" && $(readlink "$target") == "${paths[$i]}" ]]; then
            continue
        fi
        if [[ -e "$target" || -L "$target" ]]; then
            rm -rf -- "$target"
        fi
        if ! ln -s -- "${paths[$i]}" "$target"; then
            warn "Could not link $target to ${paths[$i]}"
            return 1
        fi
        printf 'Linked %s -> %s\n' "$target" "${paths[$i]}"
    done
    printf 'Skills ready: %s (%d skills)\n' "$destination" "$((last - first))"
}

link_file() {
    local source=$1 target=$2
    if [[ ! -f "$source" ]]; then
        warn "Cannot link $target: source file is missing: $source"
        return 1
    fi
    if [[ -L "$target" && "$target" -ef "$source" ]]; then
        printf 'Already linked: %s\n' "$target"
        return
    fi
    if [[ -e "$target" || -L "$target" ]]; then
        if [[ -L "$target" ]]; then
            warn "Cannot link $target to $source: already links to $(readlink "$target"); left unchanged."
        else
            warn "Cannot link $target to $source: destination already exists; left unchanged."
        fi
        return 1
    fi
    if ! ln -s -- "$source" "$target"; then
        warn "Could not link $target to $source"
        return 1
    fi
    printf 'Linked %s -> %s\n' "$target" "$source"
}

main() (
    local root general total destination physical previous agent i status=0
    local names=() paths=() destinations=() starts=() ends=() checked=()
    root=$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
    printf 'Setting up agents from %s\n' "$root"
    shopt -s nullglob
    [[ -f "$root/AGENTS.md" ]] || { printf 'Missing shared AGENTS.md\n' >&2; return 1; }
    [[ -d "$root/skills" ]] || { printf 'Missing skills directory\n' >&2; return 1; }
    for destination in "$root/skills" "$root/t3/skills"; do
        [[ ! -f "$destination/SKILL.md" ]] || {
            printf 'Put each skill in its own directory: %s\n' "$destination" >&2
            return 1
        }
        [[ ! -L "$destination" ]] || {
            printf 'Source collections must be real directories: %s\n' "$destination" >&2
            return 1
        }
    done
    collect_skills "$root/skills"
    general=${#names[@]}
    [[ ! -d "$root/t3/skills" ]] || collect_skills "$root/t3/skills"
    total=${#names[@]}
    printf 'Found %d general skills and %d T3-only skills.\n' "$general" "$((total - general))"

    destinations=("$HOME/.claude/skills" "$HOME/.claude-t3/skills" "$HOME/.codex-t3/skills")
    starts=(0 0 "$general")
    ends=("$general" "$total" "$total")

    # Separate homes are required for T3-only skills and runtime state.
    for agent in claude codex; do
        if [[ "$HOME/.$agent-t3" -ef "$HOME/.$agent" ]]; then
            printf 'T3 home must be separate from the regular home: %s\n' "$HOME/.$agent-t3" >&2
            return 1
        fi
    done

    # Check every destination before replacing anything. Shared destination
    # directories would defeat T3 isolation, even if no T3 skills exist yet.
    for destination in "${destinations[@]}"; do
        if [[ -d "$destination" ]]; then
            physical=$(cd -P -- "$destination" && pwd)
        else
            mkdir -p -- "$(dirname -- "$destination")"
            physical=$(cd -P -- "$(dirname -- "$destination")" && pwd)/${destination##*/}
        fi
        case "$physical/" in "$root/"*)
            printf 'Destination is inside source repository: %s\n' "$destination" >&2; return 1 ;;
        esac
        case "$root/" in "$physical/"*)
            printf 'Destination contains source repository: %s\n' "$destination" >&2; return 1 ;;
        esac
        for previous in "${checked[@]}"; do
            case "$physical/" in "$previous/"*)
                printf 'Skill destinations overlap: %s\n' "$destination" >&2; return 1 ;;
            esac
            case "$previous/" in "$physical/"*)
                printf 'Skill destinations overlap: %s\n' "$destination" >&2; return 1 ;;
            esac
        done
        checked+=("$physical")
    done
    for i in "${!destinations[@]}"; do
        # Keep errexit active inside the subshell while collecting failures.
        set +e
        (set -e; link_set "${destinations[$i]}" "${starts[$i]}" "${ends[$i]}")
        if [[ $? != 0 ]]; then status=1; fi
        set -e
    done
    for destination in "$HOME/.claude-t3/CLAUDE.md" "$HOME/.codex-t3/AGENTS.md"; do
        set +e
        (set -e; link_file "$root/AGENTS.md" "$destination")
        if [[ $? != 0 ]]; then status=1; fi
        set -e
    done
    link_file "$HOME/.claude/settings.json" "$HOME/.claude-t3/settings.json" || status=1
    if [[ "$status" == 0 ]]; then
        printf 'Agent setup complete. All required links are ready.\n'
    else
        warn 'Agent setup incomplete. See the errors above.'
    fi
    return "$status"
)

if [[ ${BASH_SOURCE[0]} == "$0" ]]; then main "$@"; fi
