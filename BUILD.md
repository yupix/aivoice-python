# A.I.VOICE Python Library - Build & Release Guide

## 🚀 ビルドと配布の手順

### 1. 開発環境のセットアップ

```bash
# 依存関係をインストール
pip install -r requirements.txt

# または開発用依存関係も含めて
pip install -e .[dev]
```

### 2. パッケージのビルド

```bash
# ビルドツールのインストール（初回のみ）
pip install build

# パッケージをビルド
python -m build
```

これで `dist/` フォルダに以下のファイルが生成されます：
- `aivoice_python-0.1.0-py3-none-any.whl` (wheel形式)
- `aivoice-python-0.1.0.tar.gz` (source distribution)

### 3. ローカルテスト

```bash
# 生成されたwheelファイルをテスト環境にインストール
pip install dist/aivoice_python-0.1.0-py3-none-any.whl

# または
pip install dist/aivoice-python-0.1.0.tar.gz
```

### 4. PyPIへのアップロード

#### TestPyPIでのテスト（推奨）

```bash
# twineのインストール（初回のみ）
pip install twine

# TestPyPIにアップロード
python -m twine upload --repository testpypi dist/*
```

#### 本番PyPIにアップロード

```bash
# 本番PyPIにアップロード
python -m twine upload dist/*
```

### 5. アカウント設定

#### PyPIアカウント作成
1. [PyPI](https://pypi.org/) でアカウント作成
2. [TestPyPI](https://test.pypi.org/) でもアカウント作成（テスト用）

#### API Token設定
```bash
# ~/.pypirc ファイルを作成
[distutils]
index-servers = pypi testpypi

[pypi]
username = __token__
password = <your-api-token>

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = <your-testpypi-api-token>
```

### 6. バージョン更新の手順

1. `pyproject.toml` のバージョンを更新
2. `aivoice_python/__init__.py` の `__version__` を更新
3. 変更をコミット & タグ作成
4. ビルド & アップロード

```bash
# バージョンタグ作成
git tag v0.1.0
git push origin v0.1.0

# ビルド
python -m build

# アップロード
python -m twine upload dist/*
```

### 7. GitHub Actionsでの自動化（オプション）

`.github/workflows/publish.yml` ファイルを作成すると、タグプッシュ時に自動でPyPIにアップロードできます。

### 8. インストール確認

```bash
# PyPIからインストール
pip install aivoice-python

# 動作確認
python -c "from aivoice_python import AIVoiceTTsControl; print('Success!')"
```

## 📁 ファイル構造

```
aivoice-python/
├── aivoice_python/          # パッケージソース
├── tests/                   # テストファイル
├── examples/               # 使用例
├── pyproject.toml          # プロジェクト設定
├── README.md               # ドキュメント
├── LICENSE                 # ライセンス
└── requirements.txt        # 依存関係
```

## 🔧 トラブルシューティング

### ビルドエラーが出る場合
```bash
# setuptools の更新
pip install --upgrade setuptools wheel build
```

### アップロードエラーが出る場合
```bash
# twine の更新
pip install --upgrade twine

# 認証情報の確認
python -m twine check dist/*
```

## 📚 参考リンク

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Setuptools Documentation](https://setuptools.pypa.io/)
