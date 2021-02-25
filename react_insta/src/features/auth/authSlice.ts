import { createSlice,createAsyncThunk } from '@reduxjs/toolkit';
import { RootState } from '../../app/store';
import axios from "axios";
import { PROPS_AUTHEN, PROPS_PROFILE, PROPS_NICKNAME } from "../types";

//djangoのエンドポイントのURLを定数で定義しておく reactの環境変数で格納(.envファイルに定義してある)
const apiUrl = process.env.REACT_APP_DEV_API_URL;

//////////////////////////
//APIにアクセスして処理する関数は非同期関数として実装する
/////////////////////////
//JWTのトークンを取得
export const fetchAsyncLogin = createAsyncThunk(
    "auth/post",//アクションの名前　
    async (authen: PROPS_AUTHEN) => {//非同期系 引数authenはreactのコンポーネントが呼び出されるときに格納される PROPS_AUTHEN型はtypes.tsで定義
      //authen/jwt/createはJWTのアクセスポイントのトークン
      const res = await axios.post(`${apiUrl}authen/jwt/create`, authen, {
        headers: {
          "Content-Type": "application/json",//postメソッドの場合Content_Typeでapplication/jsonを指定する必要がある
        },
      });
      return res.data;//取得したトークンを返す
    }
  );
  //新規ユーザーを作成する非同期関数
  export const fetchAsyncRegister = createAsyncThunk(
    "auth/register",
    async (auth: PROPS_AUTHEN) => {
      const res = await axios.post(`${apiUrl}api/register/`, auth, {
        headers: {
          "Content-Type": "application/json",
        },
      });
      return res.data;
    }
  );
  
  //プロフィーるを新規で作る非同期関数
  export const fetchAsyncCreateProf = createAsyncThunk(
    "profile/post",
    async (nickName: PROPS_NICKNAME) => {
      const res = await axios.post(`${apiUrl}api/profile/`, nickName, {//imgデータはmodelでnull= trueにしてるので最初はnickNameで作るようにしておく
        headers: {
          "Content-Type": "application/json",
          Authorization: `JWT ${localStorage.localJWT}`,//ログインが成功した時点でextrareduceで後処理でトークンを格納するようになっているので、profileをつくるときにはjwtは更新されているようになっている

        },
      });
      return res.data;
    }
  );
  //プロフィールを更新するときの非同期関数
  export const fetchAsyncUpdateProf = createAsyncThunk(
    "profile/put",
    async (profile: PROPS_PROFILE) => {
      const uploadData = new FormData();
      uploadData.append("nickName", profile.nickName);
      profile.img && uploadData.append("img", profile.img, profile.img.name);
      const res = await axios.put(
        `${apiUrl}api/profile/${profile.id}/`,
        uploadData,
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `JWT ${localStorage.localJWT}`,
          },
        }
      );
      return res.data;
    }
  );
  
  //ログインしているユーザーを確認する非同期関数
  export const fetchAsyncGetMyProf = createAsyncThunk("profile/get", async () => {
    const res = await axios.get(`${apiUrl}api/myprofile/`, {
      headers: {
        Authorization: `JWT ${localStorage.localJWT}`,
      },
    });
    //バックエンドのMyProfileListViewの返り値が配列のため要素へアクセスする
    return res.data[0];
  });
  


  //存在するProfileの一覧を見る関数
  export const fetchAsyncGetProfs = createAsyncThunk("profiles/get", async () => {
    const res = await axios.get(`${apiUrl}api/profile/`, {
      headers: {
        Authorization: `JWT ${localStorage.localJWT}`,
      },
    });
    return res.data;
  });

  
export const authSlice = createSlice({
    name: "auth",
    initialState: {
      //モーダルの表示非表示のstate
      openSignIn: true,//ログイン画面のモーダル。webページが立ち上がったときにユーザーにログインを促すためTrue
      openSignUp: false,//register用のモーダル
      openProfile: false,//ログインしているユーザーのプロフィール編集のモーダル
      //バックエンドの処理をしているときのstate
      isLoadingAuth: false,
      //DJangoのモデルに合うように定義
      myprofile: {//ろぐいんしているユーザーのプロフィール
        id: 0,
        nickName: "",
        userProfile: 0,
        created_on: "",
        img: "",
      },
    
      profiles: [//存在するプロフィールの一覧をRenuxで保持するためのstate
        {
          id: 0,
          nickName: "",
          userProfile: 0,
          created_on: "",
          img: "",
        },
      ],
    },
    //////////////////////////////////////////////
    //reducersはsteteの門番 actionと以前のステートから新しいstateに変更させる関数を定義
    ///////////////////////////////////////////////
    reducers: {
      //外部のAPIにフェッチがスタートしたときに呼び出されるアクション
      fetchCredStart(state) {
        state.isLoadingAuth = true;
      },
      //外部のAPIにフェッチが終了したときに呼び出されるアクション
      fetchCredEnd(state) {
        state.isLoadingAuth = false;
      },
    //ログイン用のモーダルの表示・非表示のアクション
      setOpenSignIn(state) {
        state.openSignIn = true;
      },
      resetOpenSignIn(state) {
        state.openSignIn = false;
      },
    //レジスター用のモーダルの表示・非表示のアクション
      setOpenSignUp(state) {
        state.openSignUp = true;
      },
      resetOpenSignUp(state) {
        state.openSignUp = false;
      },
    //プロフィールの編集用のモダールの表示・非表示のアクション
      setOpenProfile(state) {
        state.openProfile = true;
      },
      resetOpenProfile(state) {
        state.openProfile = false;
      },
      //ニックネームを編集するためのアクション
      editNickname(state, action) {
        state.myprofile.nickName = action.payload;
      },
    },
    //stateに応じた(非同期処理の後の)後処理
    extraReducers: (builder) => {
      //fetchAsyncLoginが成功したときの処理
      builder.addCase(fetchAsyncLogin.fulfilled, (state, action) => {
          //ローカルストレージにセットする処理
        localStorage.setItem("localJWT", action.payload.access);//action.payload　非同期関数のreturnを受け取ることができる JWTに関してはacsessというメソッドがある
      });
      builder.addCase(fetchAsyncCreateProf.fulfilled, (state, action) => {
        state.myprofile = action.payload;
      });
      builder.addCase(fetchAsyncGetMyProf.fulfilled, (state, action) => {
        state.myprofile = action.payload;
      });
      builder.addCase(fetchAsyncGetProfs.fulfilled, (state, action) => {
        state.profiles = action.payload;
      });
      builder.addCase(fetchAsyncUpdateProf.fulfilled, (state, action) => {
        state.myprofile = action.payload;
        state.profiles = state.profiles.map((prof) =>//シングルページアプリケーションを実現するためのもので、state.profilesの情報をアップデート時に即座に更新する必要があるので、今更新するIDに該当するプロフィールを検索して探し出す処理をしている
          prof.id === action.payload.id ? action.payload : prof
        );
      });
    },
  });
  
  //reactのコンポーネントでよびだせるようにexportする必要がある
  //アクションの関数を定義する
  export const {
    fetchCredStart,
    fetchCredEnd,
    setOpenSignIn,
    resetOpenSignIn,
    setOpenSignUp,
    resetOpenSignUp,
    setOpenProfile,
    resetOpenProfile,
    editNickname,
  } = authSlice.actions;
  
  //Reactのコンポーネントからstateを呼び出せるようにする設定 useSelector(RTK)で利用できるようにする
  export const selectIsLoadingAuth = (state: RootState) =>
    state.auth.isLoadingAuth;//ここの　authは store.tsのなかで指定した名前 isLoadingAuthはstateのパラメーター
  export const selectOpenSignIn = (state: RootState) => state.auth.openSignIn;
  export const selectOpenSignUp = (state: RootState) => state.auth.openSignUp;
  export const selectOpenProfile = (state: RootState) => state.auth.openProfile;
  export const selectProfile = (state: RootState) => state.auth.myprofile;
  export const selectProfiles = (state: RootState) => state.auth.profiles;
  
  export default authSlice.reducer;
  