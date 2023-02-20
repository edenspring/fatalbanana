import { useSelector } from "react-redux";
import CMIndex from "../ChannelMessages/CMIndex";
import DMIndex from "../DirectMessages/DMIndex";
import FriendshipsPage from "../Friendships/FriendshipsPage";
import ServerMembers from "../ServerMembers";
import "./UserLanding.css";

export default function UserLanding({ page, theme }) {
  const user = useSelector((state) => state.session.user);

  switch (page) {
    case "channel": {
      return (
        theme && (
          <div className="UserLanding-container reverse" id={theme}>
            <ServerMembers theme={theme} />
            <CMIndex theme={theme} />
          </div>
        )
      );
    }
    case "users": {
      return (
        theme && (
            <DMIndex theme={theme} />
        )
      )
    }
    default: {
      return (
        <div className="UserLanding-container friend">
          {/* <ol>
                <li>welcome page when first logging in</li>
                <li>messages if on server page</li>
                <li>members list if on server page</li>
            </ol> */}
          <div className="UserLanding-header" id={theme}></div>
          <FriendshipsPage theme={theme} />
        </div>
      );
    }
  }
}
