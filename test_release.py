#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Release功能测试脚本
用于验证Release创建功能是否正常工作
"""

import os
import sys
import requests

# 测试配置 - 请修改为你的信息
TEST_TOKEN = ""  # 填入你的GitHub Token
TEST_OWNER = ""  # 填入你的GitHub用户名
TEST_REPO = "test-release-repo"  # 测试仓库名

def test_api_connection(token):
    """测试API连接"""
    print("=" * 50)
    print("测试1: API连接测试")
    print("=" * 50)
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        resp = requests.get("https://api.github.com/user", headers=headers, timeout=10)
        if resp.status_code == 200:
            user = resp.json()
            print(f"✓ API连接成功")
            print(f"  用户名: {user['login']}")
            return True, user['login']
        else:
            print(f"✗ API连接失败: {resp.status_code}")
            return False, None
    except Exception as e:
        print(f"✗ 连接异常: {e}")
        return False, None

def test_repo_exists(token, owner, repo):
    """测试仓库是否存在"""
    print("\n" + "=" * 50)
    print("测试2: 仓库存在性验证")
    print("=" * 50)
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"https://api.github.com/repos/{owner}/{repo}"
    print(f"检查仓库: {owner}/{repo}")
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            repo_data = resp.json()
            print(f"✓ 仓库存在")
            print(f"  全名: {repo_data['full_name']}")
            print(f"  私有: {repo_data['private']}")
            return True
        elif resp.status_code == 404:
            print(f"✗ 仓库不存在")
            print(f"  可能原因:")
            print(f"    1. 仓库名称错误")
            print(f"    2. 仓库为私有且无权限")
            return False
        else:
            print(f"✗ 查询失败: {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ 查询异常: {e}")
        return False

def test_create_repo(token, owner, repo):
    """创建测试仓库"""
    print("\n" + "=" * 50)
    print("测试3: 创建测试仓库")
    print("=" * 50)
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "name": repo,
        "description": "Test repository for Code Manager",
        "private": False,
        "auto_init": True
    }
    
    try:
        resp = requests.post("https://api.github.com/user/repos", headers=headers, json=data, timeout=30)
        if resp.status_code == 201:
            print(f"✓ 仓库创建成功")
            print(f"  URL: {resp.json()['html_url']}")
            return True
        elif resp.status_code == 422:
            print(f"✓ 仓库已存在（跳过创建）")
            return True
        else:
            print(f"✗ 创建失败: {resp.status_code}")
            try:
                print(f"  错误: {resp.json().get('message', '')}")
            except:
                pass
            return False
    except Exception as e:
        print(f"✗ 创建异常: {e}")
        return False

def test_create_release(token, owner, repo, tag="v0.0.1-test"):
    """测试创建Release"""
    print("\n" + "=" * 50)
    print("测试4: 创建Release")
    print("=" * 50)
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "tag_name": tag,
        "name": f"Test Release {tag}",
        "body": "## 测试Release\n\n- 这是一个自动创建的测试Release\n- 用于验证Code Manager功能",
        "draft": False,
        "prerelease": False
    }
    
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    print(f"创建Release: {tag}")
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=30)
        if resp.status_code == 201:
            release = resp.json()
            print(f"✓ Release创建成功")
            print(f"  URL: {release['html_url']}")
            print(f"  Tag: {release['tag_name']}")
            return True, release
        else:
            print(f"✗ 创建失败: {resp.status_code}")
            try:
                error = resp.json()
                print(f"  错误信息: {error.get('message', '')}")
                if 'errors' in error:
                    for err in error['errors']:
                        print(f"  - {err.get('message', '')}")
            except:
                print(f"  响应: {resp.text[:200]}")
            return False, None
    except Exception as e:
        print(f"✗ 创建异常: {e}")
        return False, None

def test_list_releases(token, owner, repo):
    """列出Release"""
    print("\n" + "=" * 50)
    print("测试5: 列出Release")
    print("=" * 50)
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            releases = resp.json()
            print(f"✓ 获取成功，共 {len(releases)} 个Release")
            for r in releases[:5]:  # 只显示前5个
                print(f"  - {r['tag_name']}: {r['name']}")
            return True
        else:
            print(f"✗ 获取失败: {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ 获取异常: {e}")
        return False

def main():
    print("=" * 60)
    print("Code Manager Release功能测试")
    print("=" * 60)
    
    # 检查配置
    if not TEST_TOKEN:
        print("请先在脚本中设置 TEST_TOKEN")
        print("获取方式: GitHub → Settings → Developer settings → Personal access tokens")
        return
    
    if not TEST_OWNER:
        print("请先在脚本中设置 TEST_OWNER (你的GitHub用户名)")
        return
    
    # 运行测试
    success, username = test_api_connection(TEST_TOKEN)
    if not success:
        print("\n测试终止：API连接失败")
        return
    
    # 使用实际用户名
    owner = username if not TEST_OWNER else TEST_OWNER
    
    # 测试仓库是否存在
    repo_exists = test_repo_exists(TEST_TOKEN, owner, TEST_REPO)
    
    if not repo_exists:
        # 尝试创建仓库
        print("\n仓库不存在，尝试创建...")
        if not test_create_repo(TEST_TOKEN, owner, TEST_REPO):
            print("\n测试终止：无法创建测试仓库")
            return
    
    # 创建Release
    success, release = test_create_release(TEST_TOKEN, owner, TEST_REPO)
    
    if success:
        # 列出Release
        test_list_releases(TEST_TOKEN, owner, TEST_REPO)
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    
    if success:
        print("\n✓ Release功能正常工作")
        print(f"  请访问 https://github.com/{owner}/{TEST_REPO}/releases 查看")
        print("\n提示：如果之前遇到404错误，请检查：")
        print("  1. 输入的仓库路径是否正确（格式：用户名/仓库名）")
        print("  2. 仓库是否存在且有访问权限")
        print("  3. Token是否有足够的权限（需要repo权限）")

if __name__ == "__main__":
    main()
